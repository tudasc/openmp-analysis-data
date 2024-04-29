#!/bin/bash

mkdir -p $1/build
cd $1/build

module load boost

cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" &&\
cmake --build . &&\
echo "FAIL"

