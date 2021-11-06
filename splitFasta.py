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

fin = readFile(sys.argv[1])
N = int(sys.argv[2])
prefix = sys.argv[3]

index = 0
for line in fin:
    if line.startswith(">"):
        if index % N == 0:
            if index == 0:
                pass
            else:
                fout.close()
            fout = writeFile("{0}.{1}.fa".format(prefix,index//N+1))
        fout.write(line)
        index += 1
    else:
        fout.write(line)
fout.close()
fin.close()
