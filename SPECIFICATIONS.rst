==============
Specifications
==============

Fastq sequence description
==========================

Fields in fastq description:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Key
     - Description
   * - ``instrument``
     - Instrument ID
   * - ``run_number``
     - Run number on instrument.
   * - ``flowcell_ids``
     - Flowcell Identifier
   * - ``flowcell_ids``
     - Flowcell IDS
   * - ``lane``
     - Lane number
   * - ``tile``
     - Tile number
   * - ``x_pos``
     - Position X of cluster
   * - ``y_pos``
     - Position Y of cluster
   * - ``UMI``
     - Optional, appears when UMI is specified in sample sheet. UMI sequences for Read 1 and Read 2, seperated by a plus [+]
   * - ``read``
     - Read number - 1 can be single read or Read 2 of paired-end
   * - ``is_filtered``
     - Y if the read is filtered (did not pass), N otherwise
   * - ``control_number``
     - 0 when none of the control bits are on, otherwise it is an even number. On HiSeq X and NextSeq systems, control specification is not performed and this number is always 0.
   * - ``index``
     - Index of the read

See also https://help.basespace.illumina.com/files-used-by-basespace/fastq-files

Filter file
===========

The filter files can be found in the BaseCalls directory.
The filter file specifies whether a cluster passed filters.
Filter files are generated at cycle 26 using 25 cycles of data. For each tile, one filter file is generated.
Location: ``Data/Intensities/BaseCalls/L001``
File format: ``s_[lane]_[tile].filter``

The format is described below

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Bytes
     - Description
   * - 0-3
     - Zero value (for backwards compatibility)
   * - 4-7
     - Filter format version number
   * - 8-11
     - Number of clusters
   * - 12-(N+11)
     - Where N is the cluster number. unsigned 8-bits integer Bit 0 is pass or failed filter


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

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Bytes
     - Description
   * - 0-3
     - Zero value (for backwards compatibility)
   * - 4-7
     - Format version number
   * - 12-(2xN+11)
     - Where N is the cluster number
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


Bcl file
========

The BCL files can be found in the BaseCalls directory inside the run directory: ``Data/Intensities/BaseCalls/L<lane>/C<cycle>.1``

They are named as follows::

    s_<lane>_<tile>.bcl

Format:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Bytes
     - Description
   * - 0-3
     - Number of N clusters in unsigned 32bits little endian integer
   * - 4-(N+3)
     - Unsigned 8 bits integer
        - Bits 0-1 are bases encoded as: [A,C,G,T] -> [0,1,2,3] -> [00,01,10,11]
        - Bits 2-7 are shifted by 2 bits and contain the quality score.
        - All bits '0' is reserved for no call (N)


Stat file
=========

The stats files can be found in the BaseCalls directory inside the run directory: ``Data/Intensities/BaseCalls/L00<lane>/C<cycle>.1``

They are named as follows::

    s_<lane>_<tile>.stats

The Stats file is a binary file containing base calling statistics; the content is described
below.

The data is for clusters passing filter only:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Start
     - Description
     - Data type
   * - Byte 0
     - Cycle number
     - integer
   * - Byte 4
     - Rverage Cycle Intensity
     - double
   * - Byte 12
     - Average intensity for A over all clusters with intensity for A
     - double
   * - Byte 20
     - Average intensity for C over all clusters with intensity for C
     - double
   * - Byte 28
     - Average intensity for G over all clusters with intensity for G
     - double
   * - Byte 44
     - Average intensity for A over clusters with base call A
     - double
   * - Byte 52
     - Average intensity for C over clusters with base call C
     - double
   * - Byte 60
     - Average intensity for G over clusters with base call G
     - double
   * - Byte 68
     - Average intensity for T over clusters with base call T
     - double
   * - Byte 76
     - Number of clusters with base call A
     - integer
   * - Byte 80
     - Number of clusters with base call C
     - integer
   * - Byte 84
     - Number of clusters with base call G
     - integer
   * - Byte 88
     - Number of clusters with base call T
     - integer
   * - Byte 92
     - Number of clusters with base call X
     - integer
   * - Byte 96
     - Number of clusters with intensity for A
     - integer
   * - Byte 100
     - Number of clusters with intensity for C
     - integer
   * - Byte 104
     - Number of clusters with intensity for G
     - integer
   * - Byte 108
     - Number of clusters with intensity for T
     - integer


References
==========

* bcl2fastq source code from illumina downloads https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software/downloads.html
* Spec file from illumina support https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq_letterbooklet_15038058brpmi.pdf
* http://support-docs.illumina.com/IN/NovaSeq6000Dx_HTML/Content/IN/NovaSeq/SequencingOutputFiles_fNV.htm
* https://help.basespace.illumina.com/files-used-by-basespace/fastq-files
* https://docs.python.org/3/library/struct.html#format-characters

See also ``mkdata.sh`` file in bcl2fastq source code for insights on bcl format.
