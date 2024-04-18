#!/bin/bash

cd $1

module load python
python setup.py build &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi