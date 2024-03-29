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
@click.option('--countries', default='LBN,MMR', help='country boundaries')
def main(adminbound, input, output, countries):
    nc_files = glob.glob(f'{input}/**/*.nc', recursive=True)
    nc_files = list(set(nc_files))
    country_list = countries.split(',')

    # load shapefile of area
    gdf = gpd.read_file(adminbound)
    gdf = gdf[gdf['adm0_src'].isin(country_list)].reset_index(drop=True)
    
    for ix, row in tqdm(gdf.iterrows(), total=len(gdf)):
        # convert into bounding box
        name = row['adm0_src']
        bbox = list(gdf[ix:ix+1].total_bounds)
        
        for file in tqdm(nc_files):
            country_file = file.replace(input, os.path.join(output, name))
            if not os.path.exists(country_file):
                os.makedirs(os.path.dirname(country_file), exist_ok=True)
                try:
                    slice_file(file, bbox, country_file)
                except:
                    print(f'error slicing {file}, continuing')
                    continue
            
            
if __name__ == "__main__":
    main()
