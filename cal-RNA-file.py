import pysam
import sys

if sys.argv[1].endswith(".bam"):
    samfl = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    samfl = pysam.AlignmentFile(sys.argv[1],'r')

total = un = uniq = multi = 0
for line in samfl:
    if not line.is_secondary:
        total += 1
        if line.is_unmapped:
            un += 1
        elif line.get_tag('NH') == 1:
            uniq += 1
        else:
            multi += 1
print("the total reads : {0}\nthe unmapped reads : {1}\nthe uniq reads : {2}\nthe multi reads : {3}\n".format(total,un,uniq,multi))