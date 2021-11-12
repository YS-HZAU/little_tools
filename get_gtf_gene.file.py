import sys
import re
from collections import OrderedDict
'''
if use stringtie or cufflinks to assemble,the output gtf file don't contain the gene line.this script is used to add it.
python get_gtf_gene.file.py MH63.seedling.nove.annotated.gtf > MH63.seedling.nove.cg.gtf
'''
class gene:
    def __init__(self,gid,chrom,start,end,strand):
        self.id = gid
        self.chrom = chrom
        self.start = start
        self.end = end
        self.strand = strand
        self.str = ""

genedict = OrderedDict()
with open(sys.argv[1],'r') as fin:
    for line in fin:
        tmp = line.strip().split("\t")
        if tmp[2] == "transcript":
            geneid = re.search(r'gene_id "(.+?)"',tmp[-1])[1]
            if geneid not in genedict:
                genedict[geneid] = gene(geneid,tmp[0],int(tmp[3]),int(tmp[4]),tmp[6])
            genedict[geneid].str += line
            if int(tmp[3]) < genedict[geneid].start:
                genedict[geneid].start = int(tmp[3])
            if int(tmp[4]) > genedict[geneid].end:
                genedict[geneid].end = int(tmp[4])
        elif tmp[2] == "exon":
            geneid = re.search(r'gene_id "(.+?)"',tmp[-1])[1]
            genedict[geneid].str += line
        else:
            sys.exit("has error!")

for i in genedict.keys():
    print("{0.chrom}\tpython\tgene\t{0.start}\t{0.end}\t.\t{0.strand}\t.\tgene_id \"{1}\";".format(genedict[i],i))
    sys.stdout.write(genedict[i].str)
sys.stdout.close()