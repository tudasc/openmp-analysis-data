#!/bin/bash

cd $1

./configure &&\
make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi