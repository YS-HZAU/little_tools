import sys
import pysam

if sys.argv[1].endswith(".bam"):
    mysam = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    mysam = pysam.AlignmentFile(sys.argv[1],'r')

header = mysam.header

N = 0
fl = 1
for line in mysam:
    if N==0:
        outsam = pysam.AlignmentFile("{0}.{1}.bam".format(sys.argv[2],fl),'wb',header=header)
        fl += 1
    if N < 1000000:
        outsam.write(line)
        N += 1
    else:
        outsam.write(line)
        outsam.close()
        outsam = pysam.AlignmentFile("{0}.{1}.bam".format(sys.argv[2],fl),'wb',header=header)
        N = 1
        fl += 1
outsam.close()