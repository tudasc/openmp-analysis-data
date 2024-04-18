#!/bin/bash

cd $1

./configure &&\
./build linux &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi