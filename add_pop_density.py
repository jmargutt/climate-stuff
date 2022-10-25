import geopandas as gpd
from sqlalchemy import create_engine
import requests
from tqdm import tqdm
import pycountry
import os
import click
import subprocess
from gdal_polygonize import gdal_polygonize

engine = create_engine(
    "postgresql://")


def get_worldpop_data(base_url, model, country, filename, filepath):
    print(f"{base_url}/{model}/{country.upper()}/{filename}")
    r = requests.get(f"{base_url}/{model}/{country.upper()}/{filename}")
    with open(filepath, "wb") as file:
        file.write(r.content)


@click.command()
@click.option('--temp', default=".", help="temporary output directory")
def add_pop_density(temp):

    base_url = "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020"
    country_list = list(pycountry.countries)
    filepath, filepath_vector = "", ""

    for country in tqdm(country_list):
        try:
            print(f'downloading {country.name}')
            filename = f"{country.alpha_3.lower()}_ppp_2020_UNadj_constrained.tif"
            filepath = os.path.join(temp, filename.lower())

            get_worldpop_data(base_url, "BSGM", country.alpha_3, filename, filepath)
            if os.path.getsize(filepath) < 1000:
                get_worldpop_data(base_url, "maxar_v1", country.alpha_3, filename, filepath)
        except:
            print('download failed')

        try:
            if os.path.exists('query.sql'):
                os.remove('query.sql')
            print(f'uploading {country.name}')
            os.environ['PGPASSWORD'] = ''
            ###################################################################
            # WARNING: FOR UPDATING EXISTING TABLES, USE OPTION raster2pgsql -d
            ###################################################################
            cmds = 'raster2pgsql -t auto -I -s 4326 "' + filepath + f'" population_density.{filename.replace(".tif", "")} > query.sql'
            subprocess.call(cmds, shell=True, stdout=subprocess.DEVNULL)
            cmds = "psql -f query.sql -h 510-postgresql-server.postgres.database.azure.com -U jmargutti@510-postgresql-server -d global510"
            subprocess.call(cmds, shell=True, stdout=subprocess.DEVNULL)
            os.remove('query.sql')
        except:
            print('upload failed')

        # try:
        #     print(f'transforming from raster to vector {country.name}')
        #     filepath_vector = filepath.replace('.tif', '.geojson')
        #     gdal_polygonize(src_filename=filepath, dst_filename=filepath_vector, driver_name="GeoJSON")
        # except:
        #     print('gdal_polygonize failed')
        #
        # try:
        #     if os.path.exists('query.sql'):
        #         os.remove('query.sql')
        #     print(f'uploading {country.name}')
        #     gdf = gpd.read_file(filepath_vector)
        #     gdf = gdf.rename(columns={'DN': 'population'})
        #     gdf.to_postgis(f"{country.alpha_3.lower()}_ppp_2020_UNadj_constrained", engine, schema="population_density")
        # except:
        #     print('upload failed')

        for file_ in [filepath, filepath_vector]:
            if os.path.exists(file_):
                os.remove(file_)


if __name__ == '__main__':
    add_pop_density()


