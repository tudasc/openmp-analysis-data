#!/bin/bash

cd $1

cp linux_gnu.def make.def

make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi