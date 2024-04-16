#!/bin/bash

mkdir -p $1/build
cd $1/build

cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" &&\
cmake --build . &&\
echo "BUILD SUCCESSFUL"