#!/bin/bash

mkdir -p $1/build
cd $1/build
cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="-std=c++17 $2" -DCMAKE_LINKER=g++  -DCMAKE_SHARED_LINKER_FLAGS="-lstdc++" -DCMAKE_EXE_LINKER_FLAGS="-lstdc++" &&\
cmake --build . --parallel -j 48  &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
