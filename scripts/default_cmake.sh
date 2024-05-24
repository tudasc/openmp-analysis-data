#!/bin/bash

mkdir -p $1/build
cd $1/build

cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" &&\
cmake --build . --parallel -j 16 &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
