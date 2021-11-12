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

fsam = readSam(sys.argv[1])
fin1 = readFile(sys.argv[2])
fin2 = readFile(sys.argv[3])
fout1 = writeFile(sys.argv[4])
fout2 = writeFile(sys.argv[5])
pair = 0
unpair = 0
ridset = set()
for read in fsam:
    if read.is_secondary or read.is_duplicate or read.is_supplementary:
        continue
    if read.is_read2:
        continue
    if read.is_unmapped:
        if read.mate_is_unmapped:
            pass
        else:
            unpair += 1
            ridset.add(read.query_name)
    else:
        ridset.add(read.query_name)
        if read.mate_is_unmapped:
            unpair += 1
        else:
            pair += 1
fsam.close()

for rid1,rid2 in zip(fin1,fin2):
    seq1 = fin1.readline()
    syb1 = fin1.readline()
    qual1 = fin1.readline()
    seq2 = fin2.readline()
    syb2 = fin2.readline()
    qual2 = fin2.readline()
    sid = rid1.split()[0]
    sid = sid[1:]
    if sid not in ridset:
        fout1.write(rid1)
        fout1.write(seq1)
        fout1.write(syb1)
        fout1.write(qual1)
        fout2.write(rid2)
        fout2.write(seq2)
        fout2.write(syb2)
        fout2.write(qual2)
fin1.close()
fin2.close()
fout1.close()
fout2.close()

print("Pair map count: {0}\n".format(pair))
print("Unpair map count: {0}\n".format(unpair))