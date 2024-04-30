#!/bin/bash

cd $1

echo "1" > input && ./configure <input && make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
