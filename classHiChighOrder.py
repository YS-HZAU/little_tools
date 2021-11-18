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

### Operating sam/bam files  ###
import pysam
def readSam(insamfile):
    """
    insamfile: input sam/bam file
    return: file handle
    """
    if insamfile.endswith(".bam"):
        insam = pysam.AlignmentFile(insamfile,'rb')
    elif insamfile.endswith(".sam"):
        insam = pysam.AlignmentFile(insamfile,'r')
    else:
        raise ValueError("the input sam/bam file is not end with sam or bam!")
    return insam
        
def writeSam(outsamfile,header):
    """
    outsamfile: output sam/bam file
    header: the sam/bam file's header(chromosome information, created by insam.handle)
    return: file handle
    """
    if outsamfile.endswith(".bam"):
        outsam = pysam.AlignmentFile(outsamfile,'wb',header=header)
    elif outsamfile.endswith(".sam"):
        outsam = pysam.AlignmentFile(outsamfile,'w',header=header)
    else:
        raise ValueError("the output sam/bam file is not end with sam or bam!")
    return outsam

# ### Interval tree ###
# from bx.intervals.intersection import Intersecter, Interval
# def regionTree(tmp,resFrag):
#     """
#     tmp: The length of the list is at least 3(chrom,start,end)
#     resFrag: a dictionary to store the Interval tree
#     """
#     if tmp[0] not in resFrag:
#         resFrag[tmp[0]] = Intersecter()
#     frag = tmp[3].split("_")[-1]
#     resFrag[tmp[0]].add_interval(Interval(int(tmp[1]),int(tmp[2]),[tmp[3],frag]))

def deal(mylist, fdrop, ftwo, fsup):
    if len(mylist) == 2:
        flag = ["#","#"]
        for i in mylist:
            if i.is_read1:
                if i.is_unmapped:
                    pass
                else:
                    if i.get_tag("AS") == i.get_tag("XS"):
                        pass
                    else:
                        flag[0] = "uniq"
            else:
                if i.is_unmapped:
                    pass
                else:
                    if i.get_tag("AS") == i.get_tag("XS"):
                        pass
                    else:
                        flag[1] = "uniq"
        if "#" in flag:
            for ii in mylist:
                fdrop.write(ii)
            return "drop"
        else:
            for ii in mylist:
                ftwo.write(ii)
            return "two"
    else:
        for ii in mylist:
            fsup.write(ii)
        return "super"
    
# fin = readFile(sys.argv[1])
# resFrag = {}
# for line in fin:
#     tmp = line.strip().split()
#     regionTree(tmp,resFrag)
# fin.close()

# fin = readSam(sys.argv[2])
# prefix = sys.argv[3]

fin = readSam(sys.argv[1])
prefix = sys.argv[2]

count = {}
fdrop = writeSam("{0}.drop.bam".format(prefix),header=fin.header)
ftwo = writeSam("{0}.two.bam".format(prefix),header=fin.header)
fsup = writeSam("{0}.super.bam".format(prefix),header=fin.header)
count["drop"] = 0
count["two"] = 0
count["super"] = 0

flag = None
readList = []
for read in fin:
    if flag != None and flag != read.query_name:
        count[deal(readList, fdrop, ftwo, fsup)] += 1
        readList = []
    flag = read.query_name
    readList.append(read)
count[deal(readList, fdrop, ftwo, fsup)] += 1

fin.close()
fdrop.close()
ftwo.close()
fsup.close()

for i in ["drop","two","super"]:
    print("{0}\t{1}".format(i,count[i]))
sys.stdout.close()