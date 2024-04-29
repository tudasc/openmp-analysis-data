#!/bin/bash

mkdir -p $1/build
cd $1/build

cmake .. -DCMAKE_C_FLAGS="$2 -fopenmp -mcx16" -DCMAKE_CXX_FLAGS="$2 -fopenmp -mcx16"  -DCMAKE_EXE_LINKER_FLAGS="-mcx16" -DCMAKE_SHARED_LINKER_FLAGS="-mcx16" &&\
cmake --build . &&\
echo "FAIL"
exit
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
