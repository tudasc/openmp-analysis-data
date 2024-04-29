#!/bin/bash

cd $1/NPB-OMP

make BT && make CG && make EP && make FT && make IS && make LU && make MG && make SP &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
