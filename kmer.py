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

def getFastq(chrom,seq,fout,kmer,step):
    nn = (len(seq)-kmer)//step+1
    for i in range(nn):
        s = i*step
        e = s + kmer
        fout.write("@{0}:{1}-{2}\n".format(chrom,s,e))
        fout.write("{0}\n".format(seq[s:e]))
        fout.write("+\n")
        fout.write("{0}\n".format("J"*kmer))
    if (len(seq)-kmer) % step != 0:
        e = len(seq)
        s = e - kmer
        fout.write("@{0}:{1}-{2}\n".format(chrom,s,e))
        fout.write("{0}\n".format(seq[s:e]))
        fout.write("+\n")
        fout.write("{0}\n".format("J"*kmer))

kmer = int(sys.argv[1]) # 100
step = int(sys.argv[2]) # 10
infile = sys.argv[3]
outfile = sys.argv[4]

fin = readFile(infile)
fout = writeFile(outfile)

chrom = None
seq = ""
for line in fin:
    if line.startswith(">") and chrom == None:
        chrom =  line.strip().split()[0]
        chrom = chrom[1:]
    elif line.startswith(">") and chrom != None:
        getFastq(chrom,seq,fout,kmer,step)
        chrom =  line.strip().split()[0]
        chrom = chrom[1:]
        seq = ""
    else:
        seq += line.strip().upper()
getFastq(chrom,seq,fout,kmer,step)

fin.close()
fout.close()