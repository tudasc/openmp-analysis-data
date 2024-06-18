# OpenMP usage analysis Binaries

This repo contains the build scripts to build all relevant repos for our OpenMP study.
The result_data.tar.gz includes the collected data from our analysis.
The scripts used for analysis are in our repo: https://github.com/tudasc/openmp-analysis

## Build script
All build script in scripts are designed as follows:

#### Input

The build script gets the following input parameters.

* `$1` : fully qualified path to where the repository was checked out
* `$2` : `-O0` or `-O2` indicating if building with optimizations turned on


#### Execution
The build system should be executed with the following compiler versions `gcc/11.2.0 , openmpi/4.1.6` to produce an x86 binary. It can expect to have `cmake/3.26.1 , make/4.2.1` available in the PATH.
The build script is expected to put the binaries somewhere inside the repository (excluding the `.git` dir).
Either in a separate directory inside the repo or straight in the source-tree.

#### Output
The last line that the build scripts prints to stdout should be 1 of 3 strings:
* `BUILD SUCCESSFUL` indicating a successful build (binaries are present)
* `EXTRACT SUCCESSFUL` indicating a successful extraction of the binaries, if an automatic build failed (binaries are present)
* `FAIL` failure resulting in no binaries to be present


