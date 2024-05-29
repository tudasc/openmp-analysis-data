#!/bin/bash

cd $1

sed -i 's/CXX = CC/CXX = mpicxx/g' Makefile

make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
