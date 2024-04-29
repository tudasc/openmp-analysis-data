#!/bin/bash

cd $1
echo "FAIL"
exit

cd demos/openmp/dynamic
COMP=gnu make
make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
