#!/bin/bash

cd $1

echo "1000 1000 2" > input && make grid <input && make openmp &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
