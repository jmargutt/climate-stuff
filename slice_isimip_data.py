import glob
import xarray as xr
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import os
import click


def slice_file(file, bbox, dest):
    with xr.open_dataset(file) as ds:
        ds.sel(lat=slice(bbox[3], bbox[1]), lon=slice(bbox[0], bbox[2])).to_netcdf(dest)


@click.command()
@click.option('--adminbound', default='extents.geojson', help='country boundaries')
@click.option('--input', default='ISIMIP-data', help='country boundaries')
@click.option('--output', default='countries', help='country boundaries')
def main(adminbound, input, output):
    nc_files = glob.glob(f'{input}/**/*.nc', recursive=True)
    nc_files = list(set(nc_files))

    # load shapefile of area
    gdf = gpd.read_file(adminbound)
    
    for ix, row in tqdm(gdf.iterrows(), total=len(gdf)):
        # convert into bounding box
        name = row['adm0_src']
        if pd.isna(name) or len(name) != 3:
            continue
        bbox = list(gdf[ix:ix+1].total_bounds)
        
        try:
            for file in tqdm(nc_files):
                country_file = file.replace(input, os.path.join(output, name))
                os.makedirs(os.path.dirname(country_file), exist_ok=True)
                slice_file(file, bbox, country_file)
        except:
            print(f'error creating files for {name}, continuing')
            continue
            
            
if __name__ == "__main__":
    main()
