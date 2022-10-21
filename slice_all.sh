#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
DIR="/home/geo/climate-change/ISIMIP-data2/"
for f in "$DIR"/**/*.nc
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
#  python3 slice_isimip_data.py --file "$f"
done