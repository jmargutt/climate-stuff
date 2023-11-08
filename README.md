# climate-stuff

A bunch of scripts to extract/download/transform climate data.

### slice_isimit_data.py

This is what you need to create a country-sized slice of all ISIMIP data.
Usage:
1. Turn on [heavy-duty-geo-data](https://portal.azure.com/#@rodekruis.onmicrosoft.com/resource/subscriptions/b2d243bd-7fab-4a8a-8261-a725ee0e3b47/resourceGroups/510global/providers/Microsoft.Compute/virtualMachines/heavy-duty-geo-data/overview)
2. SSH into heavy-duty-geo-data (credentials are in Bitwarden > Data Analysis)
3. mount the datalake blob storage
```
sudo blobfuse climate-change --tmp-path=/mnt/resource/blobfusetmp  --config-file=fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 -o allow_other
```
4. run the script for your country of interest, e.g. Barbados (BRB)
```
python slice_isimip_data.py --adminbound adm0_polygons.gpkg --input /home/geo/climate-change/ISIMIP-data/global --output /home/geo/climate-change/ISIMIP-data/adm0 --countries BRB
```
5. wait until it's over; if it takes too long and you gotta log off, use [screen](https://linuxize.com/post/how-to-use-linux-screen/)
6. your data is now under `510datalakestorage/climate-change/ISIMIP-data/adm0/BRB`
