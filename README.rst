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

|

=========
fastq2bcl
=========


    fastq2bcl convert fastq files in a bcl2fastq-able run directory.


A FASTQ file is a text file that contains the sequence data from the clusters that pass filter on a flow cell.
Demultiplexing assigns clusters to a sample.

FASTQ sample sequence::

    @M11111:222:000000000-K9H97:1:1101:21270:1316 1:N:0:1
    CTTCCTAGAAGTACGTGCCAGCACGATCCAATCTCGCATCACCTTTTTTCTTTCTACTTCTACTCTCCTCTTATCTCTTCTTTTTCTTGTTTTTTTTCTTTATTCCATCT
    +
    CCCCCFA,,,,C9C6E-:C9,C,C+,:EC9,CFDE,@+6+;,,,C,CF7,@9E,,,C<,,,;<C,,6,,:C@,,,,:<<@,,,5=A,<,,,4,9=:@<?,,,,9C,,9,,


Install
=======

use pip to install in edit mode::
    pip install -e .

Test
====

use tox or pytest to test::
    tox
    pytest

Lint
====

you can lint with::
    tox -e lint

References
==========

* bcl2fastq source code from https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software/downloads.html
* Spec file from https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq_letterbooklet_15038058brpmi.pdf


.. _pyscaffold-notes:

Notes
=====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.

See also ``mkdata.sh`` file in bcl2fastq source code for insights on bcl format.
