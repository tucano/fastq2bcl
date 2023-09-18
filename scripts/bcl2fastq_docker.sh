#!/bin/bash
#
# Run bcl2fastq via docker

docker run --platform linux/amd64 -v $PWD:/mnt/data nfcore/bcl2fastq bcl2fastq -R /mnt/data
