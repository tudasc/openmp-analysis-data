#!/bin/bash

cd $1
echo "CC      =       gcc" >> make.def
echo "OPTFLAGS = -Ofast -fopenmp -lm" >> make.def
make jac_solv pi vadd vadd_heap&&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
