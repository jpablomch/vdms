## Installation

### Dependencies

    sudo apt-get install scons
    sudo apt-get install libjsoncpp-dev
    sudo apt-get install automake libtool curl make g++ unzip libgtest-dev
    sudo apt-get install cmake wget zlib1g-dev libbz2-dev libssl-dev liblz4-dev
    sudo apt-get install libtiff5-dev libjasper-dev libgtk-3-dev
    sudo apt-get install flex libjsoncpp-dev javacc libbison-dev openjdk-8-jdk
    sudo apt-get install tbb-examples
    sudo apt-get install zlib1g-dev libssl-dev liblz4-dev libbz2-dev

    // Also, install one of the following for MPI
    sudo apt-get install libopenmpi-dev
    sudo apt-get install mpich

### External Libraries
* protobuf (default install location is /usr/local)
  * wget https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-cpp-3.3.0.zip
  * unzip protobuf-cpp-3.3.0.zip
  * cd protobuf-3.3.0/
  * ./autogen.sh
  * ./configure
  * make && make check
  * sudo make install
  * sudo ldconfg

* valijson
  * git clone https://github.com/tristanpenman/valijson.git
  * cd valijson
  * cp -r include/* /usr/local/include (may need to run as sudo)
  * This is a headers-only library, no compilation/installation necessary

[Google Test](https://github.com/google/googletest) is used for the unit tests included in the test folder. To install:

    sudo apt-get install cmake libgtest-dev

Unfortunately this doesn't actually install gtest;
you need to do the following steps to get it to work correctly:

    cd /usr/src/gtest/
    sudo cmake CMakeLists.txt
    sudo make
    sudo cp *.a /usr/lib

## [OpenCV](https://opencv.org/)
VDMS may be fine with newer versions of OpenCV, but below are instructions for installing OpenCV v3.3.1

    wget https://github.com/opencv/opencv/archive/3.3.1.zip
    unzip 3.3.1.zip
    cd 3.3.1
    mkdir build
    cd build/
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ..
    make -jX   # substitute X for maximum number of CPUs (or leave it off to use all available)
    sudo make install

## [TileDB](https://tiledb.io/)
TileDB v1.3.1. It has not been tested with the
Docker image, though please let us know if you try that and it works! The
directions below will help you install TileDB v1.3.1 from source. You can also
follow the directions listed
[here](https://docs.tiledb.io/en/latest/installation.html).

### Build TileDB

    git clone https://github.com/TileDB-Inc/TileDB
    cd TileDB
    git checkout 1.3.1
    mkdir build
    cd build
    ../bootstrap --prefix=/usr/local/
    make -jX   # substitute X for maximum number of CPUs (or leave it off to use all available)
    sudo make install

**Note:** If you have previously installed other version of TileDB
on your machine, you will need to remove the existing header file
(/usr/local/include/tiledb.h),
since the newer version of TileDB installs to /usr/local/include/tiledb/.

## [Faiss](https://github.com/facebookresearch/faiss)
Facebook Faiss library for similarity search, used as alternitive engines
on VCL::DescriptorSet.

Download [Faiss 1.2.1](https://github.com/facebookresearch/faiss/archive/v1.2.1.tar.gz)

    tar -xzvf v1.2.1.tar.gz
    cd faiss-1.2.1
    mkdir build
    cd build/
    cmake ..
    make -j

    # You may need to change some flags in the CMakeFile depending on
    # configurations on your system

    # This library does not offer an install
    # make sure you move .h files to /usr/lib/include/faiss or
    # /usr/local/lib/include/faiss
    # make sure you make the library (libfaiss.so) is available
    # system-wide
    # Or follow instructions [here](https://github.com/facebookresearch/faiss/blob/v1.2.1/INSTALL.md)

### Requirement for Python Client

    sudo apt-get install python-pip
    pip install protobuf (may need to run as sudo)

    Add VDMS Python module to PYPATH:
    export PYTHONPATH="${PYTHONPATH}:<path_to_vdms>/client/python/vdms"
    # Example:
    export PYTHONPATH="${PYTHONPATH}:/opt/intel/vdms/client/python/vdms"

### Compilation

    git clone https://github.com/intellabs/vdms
    // Or download a release.

    cd vdms
    scons [FLAGS]

Flag | Explanation
------------ | -------------
--no-server | Compiles client libraries (C++/Python) only. (will not compile neither server not tests)
--timing    | Compiles server with chronos for internal timing.
-jX         | Compiles in parallel, using X cores
INTEL_PATH=path  | Path to the root folder containing pmgd and vcl. Default is "./" which is pmgd and vcl inside vdms folder. Example: scons INTEL_PATH=/opt/intel/

### Running The VDMS Server

The config-vdms.json file contains the configuration of the server.
Some of the parameters include the TCP port that will be use for incoming
connections, maximun number of simultaneous clients, and paths to the
folders where data/metadata will be stored.

**Note:** The folders must already exists in the filesystem.

We provide a script (run_server.sh) that will create some default directories,
corresponding the default values in the config-vdms.json.

To run the server using the default directories and port, simply run:

    sh run_server.sh

