#!/bin/bash

cd $1

mkdir prerequisites
cd prerequisites

git clone https://github.com/KarypisLab/GKlib.git
cd GKlib/

mkdir install
PREREQUISITE_INSTALL_PATH=$(pwd)/install
make config prefix=$PREREQUISITE_INSTALL_PATH openmp=set

make && make install

export PATH=$PATH:$PREREQUISITE_INSTALL_PATH/bin
export CPATH=$CPATH:$PREREQUISITE_INSTALL_PATH/include
export LIBRARY_PATH=$LIBRARY_PATH:$PREREQUISITE_INSTALL_PATH/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PREREQUISITE_INSTALL_PATH/lib

# build prerequisite

cd $1

make config && make &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi