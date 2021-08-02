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

R1 = sys.argv[1]
R1out = sys.argv[2]

fin1 = readFile(R1)
fout1 = writeFile(R1out)

seq = set()
total = 0
uniq = 0
for i in fin1:
    total += 1
    id1 = i
    seq1 = fin1.readline()
    symbol1 = fin1.readline()
    qual1 = fin1.readline()

    if seq1 in seq:
        continue
    else:
        fout1.write("{0}{1}{2}{3}".format(id1,seq1,symbol1,qual1))
        seq.add(seq1)
        uniq += 1

fout1.close()
sys.stderr.write("The input total reads: {0} and the uniq reads: {1}\n".format(total,uniq))