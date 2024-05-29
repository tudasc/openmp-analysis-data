#!/bin/bash

cd $1

g++ $2 -Wall -o bitonicSort bitonicSort.cpp -fopenmp &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
