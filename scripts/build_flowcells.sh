#!/bin/bash
# ------------------------------------------------------------------
# [davide.rambaldi @gmail.com]
#  Build flowcells
#  Build all examples flowcells from TEST_DIR in an output dir (BUILD_DIR)
# ------------------------------------------------------------------
BUILD_DIR='build_flowcells'
TEST_DIR='data/test'
EXAMPLE_DIR='data/example'
EXAMPLE_GITURL='https://github.com/nf-core/test-datasets/raw/modules/data/genomics/homo_sapiens/illumina/bcl/flowcell.tar.gz'
EXAMPLE_SAMPLESHEET_GITURL='https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/homo_sapiens/illumina/bcl/flowcell_samplesheet.csv'
EXAMPLE_FLOWCELL='220422_M11111_0222_000000000-K9H97'
EXAMPLE_SAMPLE_PATH='Data/Intensities/BaseCalls/Sample1_S1_L001_R1_001.fastq.gz'
BCL2FASTQ=`realpath scripts/bcl2fastq_docker.sh`

VERSION=0.1.0
USAGE="Usage: build_flowcells.sh -ihv <example|test|clean>"

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
    "example")
        echo "Build example flowcells from url $EXAMPLE_GITURL"
        echo "Creating flowcells in directory $EXAMPLE_BUILD_DIR"
        mkdir -p $EXAMPLE_BUILD_DIR

        curl -L -o $EXAMPLE_BUILD_DIR/flowcell.tar.gz $EXAMPLE_GITURL
        tar -xzf $EXAMPLE_BUILD_DIR/flowcell.tar.gz --directory $EXAMPLE_BUILD_DIR/

        echo "Getting flowcells samplesheet"
        curl -L -o $EXAMPLE_BUILD_DIR/$EXAMPLE_FLOWCELL/SampleSheet.csv $EXAMPLE_SAMPLESHEET_GITURL
        echo "Demultiplexing flowcell in directory $EXAMPLE_BUILD_DIR/$EXAMPLE_FLOWCELL"

        PWD_DIR=`pwd -P`
        cd $EXAMPLE_BUILD_DIR/$EXAMPLE_FLOWCELL
        $BCL2FASTQ --tiles s_1_1101
        cd $PWD_DIR
        cp $EXAMPLE_BUILD_DIR/$EXAMPLE_FLOWCELL/$EXAMPLE_SAMPLE_PATH $EXAMPLE_BUILD_DIR
    ;;

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
                    echo "Running command: fastq2bcl -o $BUILD_DIR/$dirname $command_args > $BUILD_DIR/$dirname/fastq2blc.log 2>&1"
                    fastq2bcl -o $BUILD_DIR/$dirname $command_args > $BUILD_DIR/$dirname/fastq2blc.log 2>&1

                    # resulting RUNDIR
                    RUNDIR="$BUILD_DIR/$dirname"/YYMMDD_*
                    echo "copying SampleSheet to $RUNDIR"
                    cp $dir/*.csv $RUNDIR

                    # test bcl2fastq
                    echo "Running bcl2fastq in flowcell $RUNDIR"
                    cd $RUNDIR
                    echo "running bcl2fastq in dir $PWD"
                    $BCL2FASTQ $bcl2fastq_args > bcl2fastq.log 2>&1
                    echo "$dirname [OK]"

                    if [[ -z ${bcl2fastq_args_run2} ]]; then
                        echo "No more demultiplexing modes for $PWD"
                    else
                        echo "running second time bcl2fastq in dir $PWD"
                        $BCL2FASTQ $bcl2fastq_args_run2 > bcl2fastq_run2.log 2>&1
                    fi

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
                unset bcl2fastq_args
                unset bcl2fastq_args_run2
            else
                echo "Missing build.config. Skipping ..."
            fi

            echo "----------------------"
        done
    ;;

    "clean")
        echo "Removing build directory $BUILD_DIR"
        rm -rf $BUILD_DIR
        rm -rf $EXAMPLE_BUILD_DIR
    ;;
esac

exit 0;
