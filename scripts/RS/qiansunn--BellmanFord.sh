#!/bin/bash

cd $1

g++ -std=c++11 -fopenmp $2 -o openmp_bellman_ford openmp_bellman_ford.cpp &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
