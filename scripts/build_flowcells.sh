#!/bin/bash
#
# Build all examples flowcells from TEST_DIR in an output dir (BUILD_DIR)

BUILD_DIR='build'
TEST_DIR='data/test'

echo "Creating flowcells in BUILD_DIR $BUILD_DIR"

mkdir -p $BUILD_DIR

for dir in $TEST_DIR/*
do
    dirname=`basename $dir`
    #echo "Dir $dir basename $dirname creating corresponding dir in $BUILD_DIR"
    mkdir -p $BUILD_DIR/$dirname
    INPUT_FILES="$dir"/*.gz
    # check if there is a mask
    mask="$dir"/mask.txt

    if [ -f "$mask" ]; then
        mask_string=`cat $mask`
        mask_arg="-m $mask_string"
        echo "FOUNDED MASK $mask_arg"
    fi
    fastq2bcl -o $BUILD_DIR/$dirname $mask_arg $INPUT_FILES
    RUNDIR="$BUILD_DIR/$dirname"/YYMMDD_*
    cp $dir/*.csv $RUNDIR
done
