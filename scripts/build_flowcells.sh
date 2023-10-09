#!/bin/bash
# ------------------------------------------------------------------
# [davide.rambaldi @gmail.com]
#  Build flowcells
#  Build all examples flowcells from TEST_DIR in an output dir (BUILD_DIR)
# ------------------------------------------------------------------
BUILD_DIR='build_flowcells'
TEST_DIR='data/test'
BCL2FASTQ=`realpath scripts/bcl2fastq_docker.sh`

VERSION=0.1.0
USAGE="Usage: build_flowcells.sh -ihv <build|clean>"

# --- Options processing -------------------------------------------
if [ $# == 0 ] ; then
    echo $USAGE
    exit 1;
fi

while getopts ":vh" optname
do
    case "$optname" in
        "v")
            echo "Version $VERSION"
            exit 0;
        ;;
        "h")
            echo $USAGE
            exit 0;
        ;;
        "?")
            echo "Unknown option $OPTARG"
            exit 0;
        ;;
        ":")
            echo "No argument value for option $OPTARG"
            exit 0;
        ;;
        *)
            echo "Unknown error while processing options"
            exit 0;
        ;;
    esac
done


shift $(($OPTIND - 1))

command=$1

# --- Body --------------------------------------------------------
#  SCRIPT LOGIC GOES HERE

case "$command" in
    "test")
        echo "Build test flowcells from directory $TEST_DIR"
        echo "Creating flowcells in directory $BUILD_DIR"

        PWD_DIR=`pwd -P`
        mkdir -p $BUILD_DIR

        for dir in $TEST_DIR/*
        do
            dirname=`basename $dir`
            echo "flowcell $dirname"

            # source build.config
            if [ -f "$dir/build.config" ]; then
                mkdir -p $BUILD_DIR/$dirname
                source $dir/build.config
                echo "Expected file $expected_file"

                # check if there are command_args defined in build.config
                if [[ -z ${command_args} ]]; then
                    echo "Error: command_args is unset."
                    exit 1
                else
                    # build flowcell
                    fastq2bcl -o $BUILD_DIR/$dirname $command_args > $BUILD_DIR/$dirname/fastq2blc.log 2>&1

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
                fi

                unset expected_file
                unset output_file
                unset command_args
            else
                echo "Missing build.config. Skipping ..."
            fi

            echo "----------------------"
        done
    ;;

    "clean")
        echo "Removing build directory $BUILD_DIR"
        rm -rf $BUILD_DIR
    ;;
esac

exit 0;
