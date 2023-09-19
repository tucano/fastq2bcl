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

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://img.shields.io/coveralls/github/tucano/fastq2bcl/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/tucano/fastq2bcl
.. image:: https://readthedocs.org/projects/fastq2bcl/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://fastq2bcl.readthedocs.io/en/stable/

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

    usage: fastq2bcl [-h] [--version] [-v] [-vv] [-m MASK] [-o OUTDIR] R1 [R2] [I1] [I2]

    Convert fastq.gz reads and metadata in a bcl2fastq-able run directory

    positional arguments:
    R1                    fastq.gz with R1 reads
    R2                    fastq.gz with R2 reads (optional)
    I1                    fastq.gz with I1 reads (optional)
    I2                    fastq.gz with I2 reads (optional)

    options:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -v, --verbose         set loglevel to INFO
    -vv, --very-verbose   set loglevel to DEBUG
    -m MASK, --mask MASK  define mask in format 110N10Y10Y110N
    -o OUTDIR, --outdir OUTDIR
                            Set the output directory for mocked run. default: cwd


Usage examples::

    fastq2bcl single.fastq.gz
    fastq2bcl R1.fastq.gz R2.fastq.gz I1.fastq.gz I2.fastq.gz
    fastq2bcl -o output_dir single.fastq.gz
    fastq2bcl -o output_dir -m "100Y20N" R1.fastq.gz R2.fastq.gz I1.fastq.gz I2.fastq.gz

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

You can provide a custom mask (string) with this format::

    NumCycles|IsIndexedRead|NumCycles|IsIndexedRead

For example for 1 pair 350 bp with 1 index of 8bp::

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


Lint
====

you can lint code with::

    tox -e lint

Pre commit hook is already configured and can be installed with this command::

    pre-commit install


Fastq sequence description
==========================

Fields in fastq description:

- ``instrument`` Instrument ID.
- ``run_number`` Run number on instrument.
- ``flowcell_ids`` Flowcell IDS.
- ``lane`` Lane number.
- ``tile`` Tile number.
- ``x_pos`` Position X of cluster.
- ``y_pos`` Position Y of cluster.
- ``UMI`` Optional, appears when UMI is specified in sample sheet. UMI sequences for Read 1 and Read 2, seperated by a plus [+].
- ``read`` Read number - 1 can be single read or Read 2 of paired-end.
- ``is_filtered`` Y if the read is filtered (did not pass), N otherwise.
- ``control_number`` 0 when none of the control bits are on, otherwise it is an even number. On HiSeq X and NextSeq systems, control specification is not performed and this number is always 0.
- ``index`` Index of the read.

See also https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/FileFormat_FASTQ-files_swBS.htm

Filter file
===========

The filter files can be found in the BaseCalls directory.
The filter file specifies whether a cluster passed filters.
Filter files are generated at cycle 26 using 25 cycles of data. For each tile, one filter file is generated.
Location: ``Data/Intensities/BaseCalls/L001``
File format: ``s_[lane]_[tile].filter``

The format is described below

- Bytes 0-3 Zero value (for backwards compatibility)
- Bytes 4-7 Filter format version number
- Bytes 8-11 Number of clusters
- Bytes 12-(N+11) Where N is the cluster number. unsigned 8-bits integer Bit 0 is pass or failed filter

Filter bytes example::

    bytes([0, 0, 0, 0]) # prefix 0
    bytes([3, 0, 0, 0]) # version 3
    struct.pack("<I", cluster_count) # number of cluster in little endian unsigned int
    bytes([1]*cluster_count) # For each cluster an unsigned 8-bits integer Where Bit 0 is pass or failed filter

    1 == PASS FILTER
    0 == NO PASS FILTER


In hexdump::

    BYTES 0-3      BYTES 4-7      BYTES 8-11     BYTES 12-14
    00 00 00 00    03 00 00 00    03 00 00 00    01 01 01

At bytes 8-11 I have 3 clusters and each cluster is represented by a an unsigned 8-bit integer.


Control file
============

The control files are binary files containing control results.

- Bytes 0-3 Zero value (for backwards compatibility)
- Bytes 4-7 Format version number
- Bytes 8-11 Number of clusters
- Bytes 12-(2xN+11) Where N is the cluster number
    - Bit 0: always empty (0)
    - Bit 1: was the read identified as a control?
    - Bit 2: was the match ambiguous?
    - Bit 3: did the read match the phiX tag?
    - Bit 4: did the read align to match the phiX tag?
    - Bit 5: did the read match the control index sequence?
    - Bits 6,7: reserved for future use
    - Bits 8..15: the report key for the matched record in the controls.fasta file (specified by the REPORT_KEY metadata)

Locations file
==============

The BCL to FASTQ converter can use different types of position files and will expect a type based on the version of RTA used
The locs files can be found in the Intensities/L<lane> directories

References
==========

* bcl2fastq source code from illumina downloads https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software/downloads.html
* Spec file from illumina support https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq_letterbooklet_15038058brpmi.pdf
* http://support-docs.illumina.com/IN/NovaSeq6000Dx_HTML/Content/IN/NovaSeq/SequencingOutputFiles_fNV.htm
* https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/FileFormat_FASTQ-files_swBS.htm
* https://docs.python.org/3/library/struct.html#format-characters

See also ``mkdata.sh`` file in bcl2fastq source code for insights on bcl format.

.. _pyscaffold-notes:

Notes
=====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
