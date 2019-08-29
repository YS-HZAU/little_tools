import sys
import re
from collections import OrderedDict
'''
if use stringtie or cufflinks to assemble,the output gtf file don't contain the gene line.this script is used to add it.
python parsegtf.py MH63.seedling.nove.annotated.gtf > MH63.seedling.nove.cg.gtf
'''
flag = OrderedDict()
with open(sys.argv[1],'r') as fin:
    for line in fin:
        tmp = line.strip().split("\t")
        print(line.strip())
        if tmp[2] == "transcript":
            geneid = re.search(r'gene_id "(.+?)";',tmp[-1])[1]
            # print(geneid)
            if geneid not in flag:
                flag[geneid] = [tmp[0],int(tmp[3]),int(tmp[4]),tmp[6]]
            else:
                if int(tmp[3]) < flag[geneid][1]:
                    flag[geneid][1] = int(tmp[3])
                if int(tmp[4]) > flag[geneid][2]:
                    flag[geneid][2] = int(tmp[4])
for i in flag.keys():
    print("{0[0]}\tpython\tgene\t{0[1]}\t{0[2]}\t.\t{0[3]}\t.\tgene_id \"{1}\"".format(flag[i],i))