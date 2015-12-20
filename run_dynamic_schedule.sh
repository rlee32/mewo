#!/bin/bash

# Be sure to run this with 'source run_schedule.sh'!

cd schedule
./transfer_feature_vector.py
cd ../

# Coarse run
cd machine_shop
./set_grid_resolution.py 0.006 0.03
source generate_mesh.sh
cd ../

cd wind_tunnel_coarse
./clean_case.py
./prepare_run.py
./first_order.py
./run.py 1.5 5.0
cd ../

# Fine run
cd machine_shop
./set_grid_resolution.py 0.002 0.01
source generate_mesh.sh
cd ../

cd wind_tunnel_fine
./clean_case.py
cp -r ../wind_tunnel_coarse/0 ./
./prepare_run.py
./second_order.py
echo "Mapping flow solution from coarse to fine."
mapFields ../wind_tunnel_coarse -consistent -sourceTime latestTime \
  > ../bridge/map_log
./run.py 0.1 2.0
rm main.msh
./store_solution.py
cd ../

cd wind_tunnel_coarse
./clean_case.py
cd ../

cd wind_tunnel_fine
./clean_case.py
cp -r ../wind_tunnel_coarse/0 ./
cd ../
