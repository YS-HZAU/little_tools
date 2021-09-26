# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:09:10 2019

@author: huang
"""

import sys

'''
python count2FPKM.py htseq.count exon_gene_length.txt out.txt
htseq.count：htseq-count -f bam -r name -s no -a 10 -t exon -i gene_id -m intersection-nonempty <input_bam> <gtf_file> > <counts_file>
exon_gene_length.txt：perl -F"\t" -lane 'if($F[2] eq "exon"){$gene="tmp";$gene=$1 if($F[8]=~/gene_id "(.+?)";/);print "$gene#$F[6]#$F[0]\t".($F[3]-1)."\t$F[4]"}' gencode.v24.annotation.gtf | bedtools sort -i - | bedtools merge -i - | perl -F"\t" -lane '@tmp=split(/#/,$F[0]);print "$tmp[2]\t$F[1]\t$F[2]\t$tmp[1]\t.\t$tmp[0]"' > exon_gene_length
result different with TCGA：
    TCGA use protein_coding gene to calculate the total and Q75l,I use all.
'''

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

geneLength = {}
fin = readFile(sys.argv[2])
for line in fin:
    tmp = line.strip().split("\t")
    if tmp[5] not in geneLength:
        geneLength[tmp[5]] = 0
    geneLength[tmp[5]] += (int(tmp[2])-int(tmp[1]))
fin.close()

total = []
fin = readFile(sys.argv[1])
fout = writeFile(sys.argv[3])
for index,line in enumerate(fin):
    if line.startswith("__"):
        continue
    tmp = line.strip().split()
    if index == 0:
        total.append(0)
        for ii in tmp[1:]:
            total.append(int(ii))
    else:
        for jj,ii in enumerate(tmp):
            if jj == 0:
                continue
            total[jj] += int(ii)

# print(total)
# sys.exit()

fin.seek(0,0)
for line in fin:
    if line.startswith("__"):
        continue
    tmp = line.strip().split()
    for jj,ii in enumerate(tmp):
        if jj == 0:
            fout.write("{0}\t{1}".format(tmp[0],geneLength[tmp[0]]))
            continue
        if int(ii) == 0:
            fpkm = 0
        else:
            fpkm = int(ii)*1000000000/geneLength[tmp[0]]/total[jj]
        fout.write("\t{0:.5f}".format(fpkm))
    fout.write("\n")
fin.close()
fout.close()
