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

def tostr(mylist):
    mylist[1] = str(mylist[1])
    mylist[2] = str(mylist[2])
    return "\t".join(mylist)

fin = readFile(sys.argv[1])
distance = int(sys.argv[2])
fout = writeFile(sys.argv[3])
fmerge = writeFile(sys.argv[4])

pre = None
for line in fin:
    if line.startswith("track"):
        continue
    tmp = line.strip().split()
    tmp[1] = int(tmp[1])
    tmp[2] = int(tmp[2])
    if pre != None:
        if tmp[0] != pre[0]:
            fout.write("{0}\n".format(tostr(pre)))
            pre = tmp
        else:
            if tmp[1]-pre[2] > distance:
                fout.write("{0}\n".format(tostr(pre)))
                pre = tmp
            else:
                if pre[10] < tmp[10]:
                    fmerge.write("{0}\n".format(tostr(pre)))
                    pre = tmp
                else:
                    fmerge.write("{0}\n".format(tostr(tmp)))
    else:
        pre = tmp
fout.write("{0}\n".format(tostr(pre)))
fin.close()
fout.close()
fmerge.close()