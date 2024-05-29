#!/bin/bash

cd $1

sed -i '/.\/paralel_dijkstra 6/d' makefile

make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
