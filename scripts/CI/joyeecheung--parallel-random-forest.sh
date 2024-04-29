#!/bin/bash

cd $1/src

g++ DecisionTree.cpp Config.cpp RandomForest.cpp main.cpp  -I. $2 && \
echo "BUILD SUCCESSFUL"
if [ $? -ne 0 ]; then
    echo "FAIL"
fi
