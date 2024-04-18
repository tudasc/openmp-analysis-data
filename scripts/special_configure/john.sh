#!/bin/bash

cd $1/src

./configure &&\
make -s clean && make -sj4 &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi