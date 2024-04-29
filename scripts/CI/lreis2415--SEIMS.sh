#!/bin/bash
echo "FAIL"
exit

cd $1
git clone git@github.com:OSGeo/gdal.git
mkdir -p $1/gdal/build
mkdir -p $1/build
cd $1/build
cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" &&\
cmake --build . &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
