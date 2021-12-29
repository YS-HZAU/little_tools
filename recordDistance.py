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

if len(sys.argv) == 1:
    fin = sys.stdin
else:
    fin = readFile(sys.argv[1])

pre = None
for line in fin:
    if line.startswith("track"):
        continue
    tmp = line.strip().split()
    tmp[1] = int(tmp[1])
    tmp[2] = int(tmp[2])
    if pre != None:
        if tmp[0] != pre[0]:
            print("diff chrom")
        else:
            print(tmp[1]-pre[2])
    pre = tmp
fin.close()
sys.stdout.close()