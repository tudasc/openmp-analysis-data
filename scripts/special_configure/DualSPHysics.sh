#!/bin/bash

cd $1/src/source

make -f Makefile_cpu &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi