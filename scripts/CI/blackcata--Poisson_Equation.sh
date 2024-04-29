#!/bin/bash

cd $1
sed -i 's/IC=icc/IC?=icc/g' Makefile && IC="gcc -lm" make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
