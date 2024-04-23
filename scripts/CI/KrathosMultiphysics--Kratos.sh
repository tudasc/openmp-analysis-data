#!/bin/bash

mkdir -p $1/build
cd $1/build

module load python/3.9

cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" -DPYTHON_EXECUTABLE=`which python3.9 &&\
cmake --build . &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
