import sys
import pysam

def deal(mylist,myfl):
    R1R2 = ["tmp","tmp"]
    for line in mylist:
        if line.is_secondary:
            continue
        else:
            if line.is_read1:
                if line.is_unmapped:
                    R1R2[0] = "unmap"
                elif line.get_tag("NH") == 1:
                    R1R2[0] = "uniq"
                else:
                    R1R2[0] = "multi"
            elif line.is_read2:
                if line.is_unmapped:
                    R1R2[1] = "unmap"
                elif line.get_tag("NH") == 1:
                    R1R2[1] = "uniq"
                else:
                    R1R2[1] = "multi"
    flagtmp = "-".join(R1R2)
    for line in mylist:
        myfl[flagtmp].write(line)
    return flagtmp
    

if sys.argv[1].endswith(".bam"):
    samfl = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    samfl = pysam.AlignmentFile(sys.argv[1],'r')

myfl = {}
count = {}
outlist = ("unmap-unmap","unmap-uniq","unmap-multi","uniq-unmap","uniq-uniq","uniq-multi","multi-unmap","multi-uniq","multi-multi")
for i in outlist:
    tmpfile = sys.argv[2]+"."+i+".bam"
    myfl[i] = pysam.AlignmentFile(tmpfile,'wb',header=samfl.header)
    count[i] = 0

flag = None
out = []
for reads in samfl:
    if flag != None and flag != reads.qname:
        count[deal(out,myfl)] += 1
        out = []
    flag = reads.qname
    out.append(reads)
count[deal(out,myfl)] += 1

samfl.close()
for i in outlist.keys():
    if i in myfl:
        myfl[i].close()
        print("{0}\t{1}".format(i,count[i]))