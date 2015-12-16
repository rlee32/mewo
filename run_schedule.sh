#!/bin/bash

# Be sure to run this with 'source run_schedule.sh'!

cd schedule
./transfer_feature_vector.py
cd ../

cd machine_shop
./integrate_inputs.py
source generate_mesh.sh
cd ../

cd wind_tunnel
./run.py
cd ../
