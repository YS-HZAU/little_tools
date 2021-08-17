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
R2 = sys.argv[2]
R1out = sys.argv[3]
R2out = sys.argv[4]

fin1 = readFile(R1)
fin2 = readFile(R2)
fout1 = writeFile(R1out)
fout2 = writeFile(R2out)

seq = set()
total = 0
uniq = 0
for i,j in zip(fin1,fin2):
    total += 1
    id1 = i
    id2 = j
    seq1 = fin1.readline()
    seq2 = fin2.readline()
    symbol1 = fin1.readline()
    symbol2 = fin2.readline()
    qual1 = fin1.readline()
    qual2 = fin2.readline()

    combineSeq = "{0}#{1}".format(seq1,seq2)
    if combineSeq in seq:
        continue
    else:
        fout1.write("{0}{1}{2}{3}".format(id1,seq1,symbol1,qual1))
        fout2.write("{0}{1}{2}{3}".format(id2,seq2,symbol2,qual2))
        seq.add(combineSeq)
        uniq += 1

fin1.close()
fin2.close()
fout1.close()
fout2.close()
sys.stderr.write("The input total reads: {0} and the uniq reads: {1}\n".format(total,uniq))
sys.stderr.close()
