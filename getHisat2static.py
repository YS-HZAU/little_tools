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
uniq = 0
multi = 0
unmap = 0
for line in fin:
    tmp = line.split()
    if "aligned concordantly exactly 1 time" in line:
        uniq += int(tmp[0])*2
    elif "aligned concordantly >1 times" in line:
        multi += int(tmp[0])*2
    elif "aligned discordantly 1 time" in line:
        uniq += int(tmp[0])*2
    elif "aligned 0 times\n" in line:
        unmap += int(tmp[0])
    elif "aligned exactly 1 time" in line:
        uniq += int(tmp[0])
    elif "aligned >1 times" in line:
        multi += int(tmp[0])
    elif "overall alignment rate" in line:
        print("uniq count: {0}".format(uniq))
        print("multi count: {0}".format(multi))
        print("unmap count: {0}".format(unmap))
        print("------------------------------------------------------------")
        uniq = 0
        multi = 0
        unmap = 0
fin.close()
