import glob
import xarray as xr
import geopandas as gpd
import gc
from pathlib import Path
from tqdm import tqdm
import os
import click

@click.command()
@click.option('--file', help='File name.')
def slice_file(file):

    ## load shapefile of area
    boundary = 'Burkina_Faso_livilihoodzones.geojson'
    bf_gpd = gpd.read_file(boundary)
    ## convert into bounding box
    bbox = list(bf_gpd.total_bounds)

    data_dir = "ISIMIP data2"
    dest = file.replace(data_dir, 'ISIMIP data BFA')
    print(f'FILE {file}')
    print(f'DEST {dest}')
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with xr.open_dataset(file) as ds:
        ds.sel(lat=slice(bbox[3], bbox[1]), lon=slice(bbox[0], bbox[2])).to_netcdf(dest)


if __name__ == '__main__':
    slice_file()
    # home = str(Path.home())
    # data_dir = "ISIMIP data2"
    # root_dir = f"{home}/climate-change/{data_dir}"
    # nc_files = glob.glob(f'{root_dir}/**/*.nc', recursive=True)
    # nc_files = list(set(nc_files))
    #
    # ## load shapefile of area
    # boundary = 'Burkina_Faso_livilihoodzones.geojson'
    # bf_gpd = gpd.read_file(boundary)
    # ## convert into bounding box
    # bbox_bfs = list(bf_gpd.total_bounds)
    #
    # for file in tqdm(nc_files):
    #     dest = file.replace(data_dir, 'ISIMIP data BFA')
    #     os.makedirs(os.path.dirname(dest), exist_ok=True)
    #     slice_file(file, bbox_bfs, dest)