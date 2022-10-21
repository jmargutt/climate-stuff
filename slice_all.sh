#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="/home/geo/climate-change/ISIMIP-data2/**/*.nc"
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  python3 slice_isimip_data.py --file "$f"
done