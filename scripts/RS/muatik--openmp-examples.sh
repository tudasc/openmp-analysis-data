#!/bin/bash

for dir in $1/*/; do
    dir=${dir%*/}
    cd $dir
    sed -i 's/\/usr\/local\/bin\/g++-4.9/g++/g' CMakeLists.txt
    mkdir build
    cd build
    cmake .. -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" &&\
    cmake --build . --parallel -j 4 &&\
    if [ $? -ne 0 ]; then
        echo "FAIL"
    fi
    cd ../..
done
