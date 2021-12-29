import sys
import pyBigWig

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

def cal(fbw,chrom,start,end):
    if start < 0:
        start = 0
    if end > fbw.chroms()[chrom]:
        end = fbw.chroms()[chrom]
    if start == end:
        sys.stderr.write("The record has no range. {0}\t{1}\t{2}\n".format(chrom,start,end))
        return 0
    return fbw.stats(chrom,start,end)[0]

def calex(fbw,chrom,start,end,extends):
    ss = start - extends
    ee = start
    cov1 = cal(fbw,chrom,ss,ee)
    ss = end
    ee = end + extends
    cov2 = cal(fbw,chrom,ss,ee)
    return (cov1+cov2)/2

fin = readFile(sys.argv[1])
fbw = pyBigWig.open(sys.argv[2])
fout = writeFile(sys.argv[3])

nline = 0
total = 0
total1k = 0
total5k = 0
total10k = 0
for line in fin:
    if line.startswith("track"):
        continue
    nline += 1
    tmp = line.strip().split()
    start = int(tmp[1])
    end = int(tmp[2])
    dens = cal(fbw,tmp[0],start,end)
    total += dens
    dens1k = calex(fbw,tmp[0],start,end,1000)
    total1k += dens1k
    dens5k = calex(fbw,tmp[0],start,end,5000)
    total5k += dens5k
    dens10k = calex(fbw,tmp[0],start,end,10000)
    total10k += dens10k
    fout.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(line.strip(),dens,dens1k,dens5k,dens10k))

print("{0}\t{1}\t{2}\t{3}".format(total/nline,total1k/nline,total5k/nline,total10k/nline))
fin.close()
fbw.close()
fout.close()