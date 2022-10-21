import glob
import xarray as xr
import geopandas as gpd
import numpy as np
import rioxarray
import rasterio as rio
import gc
from tqdm import tqdm
from pathlib import Path


def slice_file(file, bbox, dest):
    with xr.open_dataset(file) as ds:
        ds.sel(lat=slice(bbox[3], bbox[1]), lon=slice(bbox[0], bbox[2])).to_netcdf(dest)
        ds.close()
        del ds
        gc.collect()


if __name__ == '__main__':

    home = str(Path.home())
    data_dir = "ISIMIP data2"
    root_dir = f"{home}/climate-change/{data_dir}"
    nc_files = glob.glob(f'{root_dir}/**/*.nc', recursive=True)
    nc_files = list(set(nc_files))

    ## load shapefile of area
    boundary = 'Burkina_Faso_livilihoodzones.geojson'
    bf_gpd = gpd.read_file(boundary)
    ## convert into bounding box
    bbox_bfs = list(bf_gpd.total_bounds)

    for file in nc_files:
        dest = file.replace(data_dir, 'ISIMIP BFA')
        slice_file(file, bbox_bfs, dest)