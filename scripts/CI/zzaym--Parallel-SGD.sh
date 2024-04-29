#!/bin/bash

cd $1/src

sed -i  -e"s/^ \+/\t/g" Makefile && make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
