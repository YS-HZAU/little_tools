import sys
import pysam

if sys.argv[1].endswith(".bam"):
    samfl = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    samfl = pysam.AlignmentFile(sys.argv[1],'r')
fq1 = open("{0}.1.fq".format(sys.argv[2]),'w')
fq2 = open("{0}.2.fq".format(sys.argv[2]),'w')
fq = open("{0}.fq".format(sys.argv[2]),'w')

def out2fq(reads,fout):
    if reads.is_reverse:
        fout.write("@{0}\n{1}\n+\n{2}\n".format(reads.qname,reads.get_forward_sequence(),pysam.array_to_qualitystring(reads.get_forward_qualities())))
    else:
        fout.write("@{0}\n{1}\n+\n{2}\n".format(reads.qname,reads.query,reads.qqual))

def deal(mylist,fq1,fq2,fq):
    if len(mylist) == 1:
        out2fq(mylist[0],fq)
    elif len(mylist) == 2:
        if mylist[0].is_read1:
            out2fq(mylist[0],fq1)
            out2fq(mylist[1],fq2)
        else:
            out2fq(mylist[0],fq2)
            out2fq(mylist[1],fq1)
    else:
        print("maybe have some error")

tmp = None
out = []
for line in samfl:
    if line.is_secondary or line.is_supplementary:
        continue
    if tmp != None and tmp.qname != line.qname:
        deal(out,fq1,fq2,fq)
        out = []
    tmp = line
    out.append(line)
deal(out,fq1,fq2,fq)
fq1.close()
fq2.close()
fq.close()
samfl.close()