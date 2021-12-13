import sys

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

insam = sys.argv[1]
outfile = sys.argv[2]
fin = readSam(insam)
fout = writeFile(outfile)

for read in fin:
    if read.is_unmapped:
        continue
    strand = "+"
    if read.is_reverse:
        strand = "-"
    fout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n".format(
        read.reference_name,read.reference_start,read.reference_end,read.qname,read.mapping_quality,strand,read.qstart,read.qend,read.query_length,read.cigarstring,read.get_tag("NM"),read.get_tag("MD")))

fin.close()
fout.close()