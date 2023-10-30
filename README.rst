.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/fastq2bcl.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/fastq2bcl
    .. image:: https://readthedocs.org/projects/fastq2bcl/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://fastq2bcl.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/fastq2bcl/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/fastq2bcl
    .. image:: https://img.shields.io/pypi/v/fastq2bcl.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/fastq2bcl/
    .. image:: https://img.shields.io/conda/vn/conda-forge/fastq2bcl.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/fastq2bcl
    .. image:: https://pepy.tech/badge/fastq2bcl/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/fastq2bcl
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/fastq2bcl

.. image:: https://github.com/tucano/fastq2bcl/actions/workflows/ci.yml/badge.svg
    :alt: Github Actions
    :target: https://github.com/tucano/fastq2bcl/actions/workflows/ci.yml
.. image:: https://img.shields.io/coveralls/github/tucano/fastq2bcl/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/tucano/fastq2bcl
.. image:: https://img.shields.io/pypi/v/fastq2bcl.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/fastq2bcl/
.. image:: https://readthedocs.org/projects/fastq2bcl/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://fastq2bcl.readthedocs.io/en/stable/
.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://pepy.tech/badge/fastq2bcl/month
    :alt: Monthly Downloads
    :target: https://pepy.tech/project/fastq2bcl

|

=========
fastq2bcl
=========


    fastq2bcl convert fastq files in a bcl2fastq-able run directory.


A FASTQ file is a text file that contains the sequence data
from the clusters that pass filter on a flow cell.

Illumina sequencing instruments generate per-cycle BCL basecall files as primary sequencing output,
but many downstream analysis applications use per-read FASTQ files as input.

``bcl2fastq`` combines these per-cycle BCL files from a run and translates them into FASTQ files.

At the same time as converting, bcl2fastq also separates multiplexed samples
(demultiplexing). Multiplexed sequencing allows you to run multiple individual samples
in one lane. The samples are identified by index sequences that were attached to the
template during sample prep. The multiplexed sample FASTQ files are assigned to
projects and samples based on a user-generated sample sheet, and stored in
corresponding project and sample directories

FASTQ sample sequence::

    @M11111:222:000000000-K9H97:1:1101:21270:1316 1:N:0:1
    CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT
    +
    CCCCCFA,,,,C9C6E-:C9,C,C+,:EC9,CFDE,@+6+;,,,C,CF7,@9E,,,C<,,,;<C,,6,,:C@,,,,:<<@,,,5=A,<,,,4,9=:@<?,,,,9C,,9,,

Structure of an illumina run directory::

    YYMMDD_M11111_0222_000000000-K9H97
    ├── Data
    │   └── Intensities
    │       ├── BaseCalls
    │       │   └── L001
    │       │       ├── C1.1
    │       │       │   ├── s_1_1101.bcl
    │       │       │   └── s_1_1101.stats
    │       │       ├── CNN.1
    │       │       │   ├── s_1_1101.bcl
    │       │       │   └── s_1_1101.stats
    │       │       ├── s_1_1101.control
    │       │       └── s_1_1101.filter
    │       └── L001
    │           └── s_1_1101.locs
    └── RunInfo.xml



``fastq2bcl`` take as input a set of reads (fastq.gz files) and generates a flow cell directory with:

- RunInfo.xml
- bcl and stat for each cycle
- filter file
- control file
- location file

See also: `Illumina specs <https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq_letterbooklet_15038058brpmi.pdf>`_


Usage
=====

Help::

  usage: fastq2bcl [-h] [--version] [-v] [-vv] [-m MASK] -r1 R1 [-r2 R2] [-i1 I1] [-i2 I2] [-o OUTDIR] [--exclude-umi] [--exclude-index]

  Convert fastq.gz reads and metadata in a bcl2fastq-able run directory

  options:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -v, --verbose         set loglevel to INFO
    -vv, --very-verbose   set loglevel to DEBUG
    -m MASK, --mask MASK  define mask in format 110N10Y10Y110N
    -r1 R1, --read-1 R1   fastq.gz with R1 reads
    -r2 R2, --read-2 R2   fastq.gz with R2 reads (optional)
    -i1 I1, --index-1 I1  fastq.gz with I1 reads (optional)
    -i2 I2, --index-2 I2  fastq.gz with I2 reads (optional)
    -o OUTDIR, --outdir OUTDIR
                          Set the output directory for mocked run. default: cwd
    --exclude-umi         Do not write UMI from the R1 and R2 fastq reads to the cycles
    --exclude-index       Do not write Index from the R1 and R2 fastq reads to the cycles


Usage examples::

    fastq2bcl -r1 single.fastq.gz
    fastq2bcl -r1 R1.fastq.gz -r2 R2.fastq.gz -i1 I1.fastq.gz -i2 I2.fastq.gz
    fastq2bcl -o output_dir -r1 single.fastq.gz
    fastq2bcl -o output_dir --exclude-index -r1 single.fastq.gz
    fastq2bcl -o output_dir -m 100Y20N -r1 R1.fastq.gz -r2 R2.fastq.gz -i1 I1.fastq.gz -i2 I2.fastq.gz

Custom mask
===========

By default fastq2bcl will generate a ``RunInfo.xml`` file where Reads entries are generated using the sequence length of fastq.gz files.

For exammple, if I give as input 2 pairs with length 300 bp and 2 indexes with length 8p the resulting RunInfo will be::

    <?xml version="1.0"?>
    <RunInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2">
        <Run Id="YYMMDD_run_0001_ABCD" Number="1">
            <Flowcell>ABCD</Flowcell>
            <Instrument>run</Instrument>
            <Date>YYMMDD</Date>
            <Reads>
                <Read c="300" Number="1" IsIndexedRead="N" />
                <Read NumCycles="8" Number="2" IsIndexedRead="Y" />
                <Read NumCycles="8" Number="3" IsIndexedRead="Y" />
                <Read NumCycles="300" Number="4" IsIndexedRead="N" />
            </Reads>
            <FlowcellLayout LaneCount="1" SurfaceCount="1" SwathCount="1" TileCount="1" />
        </Run>
    </RunInfo>

You can provide a custom mask (string). For example for 1 pair 350 bp with 1 index of 8bp::

    350N8Y


Install
=======

use pip to install in edit mode::

    pip install -e .

Install packages for dev in a mamba environment::

    mamba create -n fastq2bcl
    mamba install -n fastq2bcl -c conda-forge tox pyscaffold biopython pytest-cov


Scripts
=======

In the directory ``scripts`` there are some useful tools:

- ``scripts/bcl2fastq_docker.sh`` run bcl2fastq with docker on the current directory. Run it inside a run directory.
- ``scripts/build_flowcells.sh`` generate all the test flowcells using the datasets in `data/test` directory


Test
====

use tox or pytest to test::

    tox
    pytest

To test with pytest you need also pytest-cov in your environment.

You can test against the minimal required python version (3.8) with::

    tox -e py38

Lint
====

you can lint code with::

    tox -e lint

Pre commit hook is already configured and can be installed with this command::

    pre-commit install


.. _pyscaffold-notes:

Acknowledgments
===============

 * https://github.com/sottorivalab
 * https://humantechnopole.it

Notes
=====

This project is inspired by the test script https://github.com/ShawHahnLab/igseq/blob/dev/tools/fastq2bcl.py from https://github.com/ShawHahnLab

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
