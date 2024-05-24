#!/bin/bash

cd $1
g++ -fopenmp openmp-examples/openmp-hello.c -o openmp-hello.exe &&\
g++ -fopenmp matrix-multiplication/matrix-mul-openmp.c -o matrix-mul-openmp.exe &&\
mpicxx -fopenmp matrix-multiplication/matrix-mul-hybrid.c -o matrix-mul-hybrid.exe &&\
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
