#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
find "/home/geo/climate-change" -type f -name "*.nc" -exec echo "Processing file...{}" \;