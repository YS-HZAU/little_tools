import pysam
import sys

# python bed2bedgraph.py test.size test.bed.gz 8 4 test.bedgraph
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

chromSize = {}
fin = readFile(sys.argv[1])
for line in fin:
    tmp = line.strip().split()
    chromSize[tmp[0]] = int(tmp[1])
fin.close()
# print(chromSize)

fin = pysam.TabixFile(sys.argv[2])
step = int(sys.argv[3])
col = int(sys.argv[4]) # 0(no, default: 1) 1-n(calculator)
if col < 0:
    sys.exit("col must >= 0")
fout = writeFile(sys.argv[5])
chroms = fin.contigs
for chrom in chroms:
    # print(chrom)
    if chrom not in chromSize:
        continue
    index = 0
    start = index
    end = index
    flag = None
    os = 0
    oe = 0
    while(index+step < chromSize[chrom]):
        cov = 0
        for bed in fin.fetch(chrom,index,index+step,parser=pysam.asTuple()):
            if int(bed[1]) > index:
                os = int(bed[1])
            else:
                os = index
            if int(bed[2]) > index+step:
                oe = index+step
            else:
                oe = int(bed[2])
            # print(os,oe)
            if col == 0:
                cov += 1*(oe-os)/step
            else:
                cov += 1*float(bed[col-1])*(oe-os)/step
        if flag == None:
            start = index
            flag = cov
        else:
            if flag != cov:
                fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom,start,index,flag))
                start = index
                flag = cov
        index += step
    cov = 0
    for bed in fin.fetch(chrom,index,chromSize[chrom],parser=pysam.asTuple()):
        if int(bed[1]) > index:
            os = int(bed[1])
        else:
            os = index
        if int(bed[2]) > chromSize[chrom]:
            oe = chromSize[chrom]
        else:
            oe = int(bed[2])
        if col == 0:
            cov += 1*(oe-os)/(chromSize[chrom]-index)
        else:
            cov += 1*float(bed[col-1])*(oe-os)/(chromSize[chrom]-index)
    if flag == None:
        fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom,index,chromSize[chrom],cov))
    else:
        if flag == cov:
            fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom,start,chromSize[chrom],flag))
        else:
            fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom,start,index,flag))
            fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom,index,chromSize[chrom],cov))

fin.close()
fout.close()