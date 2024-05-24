#!/bin/bash
echo "FAIL"
#requires boost, requires one-api, requires zfp
cd $1
./config.sh -b omp -g && cd bin &&\
make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
