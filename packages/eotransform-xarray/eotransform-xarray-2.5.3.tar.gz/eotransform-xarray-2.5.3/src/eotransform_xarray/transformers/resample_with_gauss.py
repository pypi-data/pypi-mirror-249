from abc import abstractmethod
from dataclasses import dataclass, asdict
from typing import Tuple, Union, Literal, Mapping, Any, Optional, Dict, Callable

import numpy as np
import rioxarray  # noqa # pylint: disable=unused-import
import xarray as xr
from affine import Affine
from numpy.typing import NDArray, DTypeLike
from xarray import DataArray, Dataset
from yaml import YAMLObject, SafeLoader

from eotransform_xarray.geometry.pixel_transforms import pixel_centers_for_geotransform_extent
from eotransform_xarray.storage.storage import Storage

try:
    from numba import njit, prange, guvectorize, float64, float32
    from pyresample import SwathDefinition, AreaDefinition
    from pyresample.kd_tree import get_neighbour_info
except ImportError:
    print("ResampleWithGauss requires numba and pyresample.\npip install numba pyresample")
    raise

from eotransform_xarray.transformers import TransformerOfDataArray

EngineType = Literal['dask', 'numba']
EmptyRasterFactory = Callable[[Tuple[int, ...], DTypeLike], NDArray]


@dataclass
class Swath:
    lons: NDArray
    lats: NDArray


@dataclass
class Extent:
    lower_left_x: float
    lower_left_y: float
    upper_right_x: float
    upper_right_y: float

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return self.lower_left_x, self.lower_left_y, self.upper_right_x, self.upper_right_y


@dataclass
class Area:
    name: str
    projection: str
    columns: int
    rows: int
    extent: Extent
    transform: Affine
    description: str = ""


@dataclass
class ProjectionParameter:
    in_resampling: Dataset
    out_resampling: Dataset

    @classmethod
    def from_storage(cls, storage: Storage) -> "ProjectionParameter":
        return ProjectionParameter(**{f: v for f, v in storage.load().items()})

    def store(self, storage: Storage) -> None:
        storage.save(asdict(self))


class MaybePacked:
    def __init__(self, value: NDArray, is_packed: bool = False):
        self.value = value
        self._is_packed = is_packed
        self._max = value.max()

    def __or__(self, dtype: DTypeLike) -> "MaybePacked":
        if self._is_packed:
            return self

        if self._max <= np.iinfo(dtype).max:
            return MaybePacked(self.value.astype(dtype), True)
        else:
            return self


class StorageIntoTheVoid(Storage):
    def exists(self) -> bool:
        return False

    def load(self) -> Mapping[str, Any]:
        raise NotImplementedError("Can't load from the void.")

    def save(self, data: Mapping[str, Any]) -> None:
        pass


class EngineConfig(YAMLObject):
    @property
    @abstractmethod
    def type(self) -> EngineType:
        ...


@dataclass
class DaskConfig(EngineConfig):
    yaml_tag = "!ResampleDaskConfig"
    yaml_loader = SafeLoader

    raster_chunk_sizes: Tuple[int, int]

    @property
    def type(self) -> EngineType:
        return "dask"


@dataclass
class NumbaConfig(EngineConfig):
    yaml_tag = "!ResampleNumbaConfig"
    yaml_loader = SafeLoader

    @property
    def type(self) -> EngineType:
        return "numba"


@dataclass
class ProcessingConfig(YAMLObject):
    yaml_tag = "!ResampleProcessing"
    yaml_loader = SafeLoader

    num_parameter_calc_procs: int = 1
    num_lookup_segments: Optional[int] = None
    parameter_storage: Optional[Storage] = None
    resampling_engine: Optional[Union[NumbaConfig, DaskConfig]] = None
    load_in_resampling_params: Optional[Dict] = None
    load_out_resampling_params: Optional[Dict] = None


class ResampleWithGauss(TransformerOfDataArray):
    class MismatchError(ValueError):
        ...

    def __init__(self, swath_src: Swath, area_dst: Area, sigma: float, neighbours: int, lookup_radius: float,
                 processing_config: Optional[ProcessingConfig] = None):
        self._area_dst = area_dst
        self._proc_cfg = processing_config or ProcessingConfig()
        _fill_process_cfg_with_defaults(self._proc_cfg)

        if self._proc_cfg.parameter_storage.exists():
            self._projection_params = ProjectionParameter.from_storage(self._proc_cfg.parameter_storage)
        else:
            self._projection_params = self._calc_projection(swath_src, area_dst, neighbours, lookup_radius)
            self._projection_params.store(self._proc_cfg.parameter_storage)

        if self._proc_cfg.load_in_resampling_params is not None:
            self._projection_params.in_resampling = self._projection_params.in_resampling.load(
                **self._proc_cfg.load_in_resampling_params)
        if self._proc_cfg.load_out_resampling_params is not None:
            self._projection_params.out_resampling = self._projection_params.out_resampling.load(
                **self._proc_cfg.load_out_resampling_params)

        self._projection_params.out_resampling['weights'] = \
            self._distances_to_gauss_weights(self._projection_params.out_resampling['weights'], sigma)

    def _calc_projection(self, swath: Swath, area: Area, neighbours: int, lookup_radius: float) -> ProjectionParameter:
        sw_def = SwathDefinition(swath.lons.swapaxes(0, -1), swath.lats.swapaxes(0, -1))
        ar_def = AreaDefinition(area.name, area.description, "proj_id", area.projection, area.columns, area.rows,
                                area.extent.to_tuple())
        val_in_idc, val_out_idc, idc, distances = get_neighbour_info(sw_def, ar_def, lookup_radius, neighbours,
                                                                     nprocs=self._proc_cfg.num_parameter_calc_procs,
                                                                     segments=self._proc_cfg.num_lookup_segments)
        packed_idc = MaybePacked(idc) | np.uint8 | np.uint16 | np.uint32 | np.uint64
        packed_idc = packed_idc.value.reshape((area.rows, area.columns, -1))
        distances = distances.astype(np.float32).reshape((area.rows, area.columns, -1,))
        out_mask = val_out_idc[..., np.newaxis].reshape((area.rows, area.columns, -1,))

        in_resampling = Dataset({'mask': (('location', 'cell'), val_in_idc[..., np.newaxis])},
                                coords={'lon': ('location', swath.lons[0]), 'lat': ('location', swath.lats[0])}) \
            .chunk({'cell': -1, 'location': -1})
        out_resampling = Dataset({'indices': (('y', 'x', 'neighbours'), packed_idc),
                                  'weights': (('y', 'x', 'neighbours'), distances),
                                  'mask': (('y', 'x', 'cell'), out_mask)}) \
            .rio.write_crs(area.projection).rio.write_transform(area.transform)

        y, x = pixel_centers_for_geotransform_extent(area.transform, area.columns, area.rows)
        out_resampling = out_resampling.assign_coords({'y': ('y', y), 'x': ('x', x)})

        if self._proc_cfg.resampling_engine.type == 'numba':
            out_resampling = out_resampling.chunk({'neighbours': -1, 'cell': -1, 'y': -1, 'x': -1})
        else:
            rc = self._proc_cfg.resampling_engine.raster_chunk_sizes
            out_resampling = out_resampling.chunk({'neighbours': -1, 'cell': -1, 'y': rc[0], 'x': rc[1]})
        return ProjectionParameter(in_resampling, out_resampling)

    def _distances_to_gauss_weights(self, distances: DataArray, sigma: float) -> DataArray:
        if self._proc_cfg.resampling_engine.type == 'numba':
            distances.values = _distance_to_gauss_weight(distances.values, sigma ** 2)
            return distances
        else:
            sig_sqrd = sigma ** 2
            return np.exp(-distances ** 2 / sig_sqrd)

    def __call__(self, x: DataArray) -> DataArray:
        self._sanity_check_input(x)
        in_valid = self._projection_params.in_resampling['mask'][:, 0]
        x = x[..., in_valid.values]
        indices = self._projection_params.out_resampling['indices']
        weights = self._projection_params.out_resampling['weights']
        out_valid = self._projection_params.out_resampling['mask'][:, :, 0]
        if self._proc_cfg.resampling_engine.type == 'numba':
            resampled = DataArray(
                _resample_numba(x.values, indices.values, weights.values, out_valid.values),
                dims=x.dims[:2] + out_valid.dims,
                coords={**{k: v for k, v in x.coords.items() if k in x.dims[:2]}, **out_valid.coords})
        else:
            resampled = xr.apply_ufunc(_resample_dask, x, indices, weights, out_valid,
                                       input_core_dims=[x.dims[-1:], ['neighbours'], ['neighbours'], []],
                                       output_dtypes=[x.dtype],
                                       dask='parallelized', keep_attrs=True)
        resampled.attrs = x.attrs
        return resampled

    def _sanity_check_input(self, x: DataArray):
        if self._projection_params.in_resampling['mask'].size != x.shape[-1]:
            raise ResampleWithGauss.MismatchError("Mismatch between resample transformation projection and input data:"
                                                  "\nvalid_indices' size doesn't match input data value length:\n"
                                                  f"{self._projection_params.in_resampling.sizes} != {x.shape}")


def _fill_process_cfg_with_defaults(config: ProcessingConfig):
    config.parameter_storage = config.parameter_storage or StorageIntoTheVoid()
    config.resampling_engine = config.resampling_engine or NumbaConfig()


@guvectorize([(float32[:], float32, float32[:]),
              (float64[:], float64, float64[:])], '(),()->()', target='parallel', nopython=True)
def _distance_to_gauss_weight(distance, sigma_sqrd, out):
    out[0] = np.exp(-distance[0] ** 2 / sigma_sqrd)


def _resample_dask(in_data: NDArray, indices: NDArray, weights: NDArray, out_valid: NDArray) -> NDArray:
    in_data = in_data.squeeze((2, 3))
    times, parameters = in_data.shape[:2]
    out = np.empty((times, parameters) + out_valid.shape, dtype=in_data.dtype)
    _resample_to_single_threaded(in_data, indices, weights, out_valid, out)
    return out


def _resample_numba(in_data: NDArray, indices: NDArray, weights: NDArray, out_valid: NDArray) -> NDArray:
    times, parameters = in_data.shape[:2]
    out = np.empty((times, parameters) + out_valid.shape, dtype=in_data.dtype)
    _resample_to_parallel(in_data, indices, weights, out_valid, out)
    return out


@njit(parallel=False)
def _resample_to_single_threaded(in_data: NDArray, indices: NDArray, weights: NDArray, out_valid: NDArray,
                                 out: NDArray) -> None:
    _resample_to_operation(in_data, indices, out, out_valid, weights)


@njit(parallel=True)
def _resample_to_parallel(in_data: NDArray, indices: NDArray, weights: NDArray, out_valid: NDArray,
                          out: NDArray) -> None:
    _resample_to_operation(in_data, indices, out, out_valid, weights)


@njit(inline='always')
def _resample_to_operation(in_data, indices, out, out_valid, weights):
    times, parameters, in_size = in_data.shape
    for y in prange(out.shape[-2]):
        for x in prange(out.shape[-1]):
            if out_valid[y, x]:
                for time in range(times):
                    for parameter in range(parameters):
                        weighted_sum = 0
                        summed_weights = 0
                        for neighbour in range(indices.shape[-1]):
                            sample_idx = indices[y, x, neighbour]
                            if sample_idx != in_size:
                                sample = in_data[time, parameter, sample_idx]
                                if not np.isnan(sample):
                                    w = weights[y, x, neighbour]
                                    weighted_sum += w * sample
                                    summed_weights += w
                        out[time, parameter, y, x] = weighted_sum / summed_weights if summed_weights > 0 else np.nan
            else:
                out[:, :, y, x] = np.nan
