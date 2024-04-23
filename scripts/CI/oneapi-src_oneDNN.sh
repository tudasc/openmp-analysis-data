#!/bin/bash

cmake -DCMAKE_C_FLAGS="$2 -DBENCHDNN_DNNL_ARG_UNDEF=999" -DCMAKE_CXX_FLAGS="$2 -DBENCHDNN_DNNL_ARG_UNDEF=999" &&\
cmake --build . -j64 &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
