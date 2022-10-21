#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
find "/home/geo/climate-change/ISIMIP-data2" -type f -name "*.nc" -exec python slice_isimip_data.py --file {} \;