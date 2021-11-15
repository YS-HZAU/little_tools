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

def deal(mylist, myfl):
    R1R2 = ["tmp","tmp"]
    for line in mylist:
        if line.is_secondary or line.is_supplementary:
            continue
        else:
            if line.is_read1:
                if line.is_unmapped:
                    R1R2[0] = "unmap"
                elif line.get_tag("AS") == line.get_tag("XS"):
                    R1R2[0] = "multimap"
                else:
                    if line.mapping_quality < 20:
                        R1R2[0] = "lowuniqmap"
                    else:
                        R1R2[0] = "uniqmap"
            elif line.is_read2:
                if line.is_unmapped:
                    R1R2[1] = "unmap"
                elif line.get_tag("AS") == line.get_tag("XS"):
                    R1R2[1] = "multimap"
                else:
                    if line.mapping_quality < 20:
                        R1R2[1] = "lowuniqmap"
                    else:
                        R1R2[1] = "uniqmap"
    flagtmp = "-".join(R1R2)
    for line in mylist:
        myfl[flagtmp].write(line)
    return flagtmp

infile = sys.argv[1]
prefix = sys.argv[2]
myfl = {}
count = {}
outlist = ["unmap","multimap","lowuniqmap","uniqmap"]
outflag = []
fin = readSam(infile)
for i in outlist:
    for j in outlist:
        outflag.append("{0}-{1}".format(i,j))
        count[outflag[-1]] = 0
for i in outflag:
    myfl[i] = writeSam("{0}.{1}.bam".format(prefix,i),fin.header)

flag = None
readList = []
for read in fin:
    if flag != None and flag != read.query_name:
        count[deal(readList, myfl)] += 1
        readList = []
    flag = read.query_name
    readList.append(read)
count[deal(readList, myfl)] += 1

fin.close()
for i in outflag:
    myfl[i].close()
    print("{0}\t{1}".format(i,count[i]))
sys.stdout.close()