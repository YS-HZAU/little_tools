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

fin1 = readFile(sys.argv[1])
fin2 = readFile(sys.argv[2])
prefix = sys.argv[3]
num = int(sys.argv[4])

index = 0
for i in fin1:
    if index == 0:
        fout1 = writeFile("{0}.tmp.{1}.R1.fastq".format(prefix,0))
        fout2 = writeFile("{0}.tmp.{1}.R2.fastq".format(prefix,0))
    elif index % num == 0:
        fout1.close()
        fout2.close()
        fout1 = writeFile("{0}.tmp.{1}.R1.fastq".format(prefix,index//num))
        fout2 = writeFile("{0}.tmp.{1}.R2.fastq".format(prefix,index//num))
    index += 1
    fout1.write(i)
    fout1.write(fin1.readline())
    fout1.write(fin1.readline())
    fout1.write(fin1.readline())
    fout2.write(fin2.readline())
    fout2.write(fin2.readline())
    fout2.write(fin2.readline())
    fout2.write(fin2.readline())

fin1.close()
fin2.close()
fout1.close()
fout2.close()