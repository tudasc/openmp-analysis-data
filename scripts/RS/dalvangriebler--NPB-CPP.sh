#!/bin/bash

cd $1/NPB-OMP

make suite &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
