import pyBigWig
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
bwfile = sys.argv[2]
outfile = sys.argv[3]
fin = readFile(infile)
fbw = pyBigWig.open(bwfile)
fout = writeFile(outfile)

chrom = None
start = None
end = None
for line in fin:
    region = line.strip().split()
    chrom = region[0]
    start = int(region[1])
    end = int(region[2])
    fout.write("{0}\t{1}\n".format(line.strip(),fbw.stats(chrom,start,end)[0]))

fin.close()
fbw.close()
fout.close()