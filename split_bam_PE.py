import sys
import pysam

if sys.argv[1].endswith(".bam"):
    mysam = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    mysam = pysam.AlignmentFile(sys.argv[1],'r')

header = mysam.header

N = 0
fl = 1
flag = None
for line in mysam:
    if N==0:
        outsam = pysam.AlignmentFile("{0}.{1}.bam".format(sys.argv[2],fl),'wb',header=header)
        fl += 1
    if N < 1000000:
        outsam.write(line)
        N += 1
    else:
        if line.query_name == flag:
            outsam.write(line)
            N += 1
        else:
            outsam.close()
            outsam = pysam.AlignmentFile("{0}.{1}.bam".format(sys.argv[2],fl),'wb',header=header)
            outsam.write(line)
            N = 1
            fl += 1
    flag = line.query_name
outsam.close()