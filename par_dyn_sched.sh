#!/bin/bash

# Be sure to run this with 'source run_schedule.sh'!

cd schedule
./transfer_feature_vector.py
cd ../

# Coarse run
# Generate mesh
cd machine_shop
./set_grid_resolution.py 0.006 0.03
source generate_mesh.sh
cd ../

# Make coarse directory
cp -r wind_tunnel wind_tunnel_coarse

# Coarse run
cd wind_tunnel_coarse
./prepare_run.py
./first_order.py
./run_parallel.py 1.5 5.0
cd ../

# Fine run
# Generate mesh
cd machine_shop
./set_grid_resolution.py 0.002 0.01
source generate_mesh.sh
cd ../

# Make fine directory
cp -r wind_tunnel wind_tunnel_fine

# Fine run
cd wind_tunnel_fine
./prepare_run.py
./second_order.py
echo "Mapping flow solution from coarse to fine."
mapFields ../wind_tunnel_coarse -consistent -sourceTime latestTime \
  > ../bridge/map_log
./run_parallel.py 0.1 2.0
cp -r ../wind_tunnel/0 ./
./store_solution.py
cd ../

rm -r wind_tunnel_coarse
rm -r wind_tunnel_fine