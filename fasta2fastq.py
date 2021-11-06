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
fout = writeFile(sys.argv[2])

seq = ""
flag = None
for line in fin:
    if line.startswith(">"):
        if flag == None:
            flag = 1
        else:
            fout.write("{0}\n+\n{0}\n".format(seq))
            seq = ""
        tmp = line.strip().split()[0]
        fid = tmp[1:]
        fout.write("@{0}\n".format(fid))
    else:
        seq += line.strip()
fout.write("{0}\n+\n{0}\n".format(seq))
fin.close()
fout.close()