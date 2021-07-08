import sys

### Operating common files  ###
import gzip
def readFile(infile):
    """
    infile: input file
    return: file handle
    """
    if infile.endswith((".gz","gzip")):
        fin = gzip.open(infile,'rt')
    else:
        fin = open(infile,'r')
    return fin
        
def writeFile(outfile):
    """
    outfile: output file
    return: file handle
    """
    if outfile.endswith((".gz","gzip")):
        fout = gzip.open(outfile,'wt')
    else:
        fout = open(outfile,'w')
    return fout

### Operating sam/bam files  ###
import pysam
def readSam(insamfile):
    """
    insamfile: input sam/bam file
    return: file handle
    """
    if insamfile.endswith(".bam"):
        insam = pysam.AlignmentFile(insamfile,'rb')
    elif insamfile.endswith(".sam"):
        insam = pysam.AlignmentFile(insamfile,'r')
    else:
        raise ValueError("the input sam/bam file is not end with sam or bam!")
    return insam
        
def writeSam(outsamfile,header):
    """
    outsamfile: output sam/bam file
    header: the sam/bam file's header(chromosome information, created by insam.handle)
    return: file handle
    """
    if outsamfile.endswith(".bam"):
        outsam = pysam.AlignmentFile(outsamfile,'wb',header=header)
    elif outsamfile.endswith(".sam"):
        outsam = pysam.AlignmentFile(outsamfile,'w',header=header)
    else:
        raise ValueError("the output sam/bam file is not end with sam or bam!")
    return outsam

infile = sys.argv[1]
outfile1 = sys.argv[2]
outfile2 = sys.argv[3]
fin = readSam(infile)
fout1 = writeSam(outfile1,fin.header)
fout2 = writeSam(outfile2,fin.header)

for read in fin:
    if read.is_read1:
        read.flag = read.flag ^ 64
        if read.mate_is_reverse:
            read.flag = read.flag ^ 32
        if read.mate_is_unmapped:
            read.flag = read.flag ^ 8
        if read.is_proper_pair:
            read.flag = read.flag ^ 2
        if read.is_paired:
            read.flag = read.flag ^ 1
        fout1.write(read)
    else:
        read.flag = read.flag ^ 128
        if read.mate_is_reverse:
            read.flag = read.flag ^ 32
        if read.mate_is_unmapped:
            read.flag = read.flag ^ 8
        if read.is_proper_pair:
            read.flag = read.flag ^ 2
        if read.is_paired:
            read.flag = read.flag ^ 1
        fout2.write(read)

fin.close()
fout1.close()
fout2.close()