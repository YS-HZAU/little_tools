from Bio import SeqIO
import sys
from itertools import zip_longest

aa=SeqIO.parse(sys.argv[1], "fastq")
bb=SeqIO.parse(sys.argv[2], "fastq")
fw = open(sys.argv[3],'w')
for i,j in zip_longest(aa,bb,fillvalue = "None"):
    if str(i) != "None":
        SeqIO.write(i,fw,'fastq')
    if str(j) != "None":
        SeqIO.write(j,fw,'fastq')
aa.close()
bb.close()
fw.close()
