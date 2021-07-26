from os import read
import sys
from collections import OrderedDict

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

outfile = sys.argv[1]
fout = writeFile(outfile)

geneDict = OrderedDict()
for index,file in enumerate(sys.argv[2:]):
    fin = readFile(file)
    for line in fin:
        tmp = line.split()
        if tmp[0] not in geneDict:
            geneDict[tmp[0]] = []
        while len(geneDict[tmp[0]]) < index:
            geneDict[tmp[0]].append("0")
        geneDict[tmp[0]].append(tmp[1])
    fin.close()

for k in geneDict.keys():
    while len(geneDict[k]) < len(sys.argv[2:]):
        geneDict[k].append("0")
    fout.write("{0}\t{1}\n".format(k,"\t".join(geneDict[k])))
    
fout.close()