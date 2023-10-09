#!/bin/bash
#
# Build all examples flowcells from TEST_DIR in an output dir (BUILD_DIR)

BUILD_DIR='build_flowcells'
TEST_DIR='data/test'
BCL2FASTQ=`realpath scripts/bcl2fastq_docker.sh`

echo "Creating flowcells in directory $BUILD_DIR"

PWD_DIR=`pwd -P`
mkdir -p $BUILD_DIR

for dir in $TEST_DIR/*
do
    dirname=`basename $dir`
    echo "flowcell $dirname"

    # source test.config
    if [ -f "$dir/test.config" ]; then
        mkdir -p $BUILD_DIR/$dirname
        source $dir/test.config
        echo "Expected file $expected_file"
        INPUT_FILES="$dir"/*.gz
        echo "Input files: $INPUT_FILES"

        # check if there is a mask defined in test.config
        if [ -z ${MASK} ]; then
            echo "The MASK is unset."
        else
            mask_arg="-m $MASK"
            echo "Mask: $MASK mask_arg: $mask_arg"
        fi

        # build flowcell
        fastq2bcl -o $BUILD_DIR/$dirname $mask_arg $INPUT_FILES > $BUILD_DIR/$dirname/fastq2blc.log 2>&1

        # resulting RUNDIR
        RUNDIR="$BUILD_DIR/$dirname"/YYMMDD_*
        echo "copying SampleSheet to $RUNDIR"
        cp $dir/*.csv $RUNDIR

        # test bcl2fastq
        echo "Running bcl2fastq in flowcell $RUNDIR"
        cd $RUNDIR
        echo "running bcl2fastq in dir $PWD"
        $BCL2FASTQ > bcl2fastq.log 2>&1
        echo "$dirname [OK]"
        cd $PWD_DIR

        # check output
        zdiff $expected_file $BUILD_DIR/$output_file > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "Output $output_file [OK]"
        else
            echo "Output $output_file differ."
        fi

        unset MASK
        unset expected_file
        unset output_file
    else
        echo "Missing test.config. Skipping ..."
    fi

    echo "----------------------"
done
