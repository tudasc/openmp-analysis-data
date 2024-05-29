#!/bin/bash

cd $1/src

make time src=omp&&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
