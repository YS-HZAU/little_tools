# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:09:10 2019

@author: huang
"""

import pandas as pd
import sys

'''
python count2FPKM.py htseq.count exon_gene_length.txt out.txt
htseq.count：htseq-count -f bam -r name -s no -a 10 -t exon -i gene_id -m intersection-nonempty <input_bam> <gtf_file> > <counts_file>
exon_gene_length.txt：perl -F"\t" -lane 'if($F[2] eq "exon"){$gene="tmp";$gene=$1 if($F[8]=~/gene_id "(.+?)";/);print "$gene#$F[6]#$F[0]\t".($F[3]-1)."\t$F[4]"}' gencode.v24.annotation.gtf | bedtools sort -i - | bedtools merge -i - | perl -F"\t" -lane '@tmp=split(/#/,$F[0]);print "$tmp[2]\t$F[1]\t$F[2]\t$tmp[1]\t.\t$tmp[0]"' > exon_gene_length
result different with TCGA：
    TCGA use protein_coding gene to calculate the total and Q75l,I use all.
'''

mydat = pd.read_table(sys.argv[1],names=["gene","count"])
mydat = mydat[~mydat['gene'].str.match("__")]
gene = []
length = []
with open(sys.argv[2],'r') as fin:
    flag = None
    sumlen = 0
    for line in fin:
        tmp = line.strip().split("\t")
        if flag != None and flag !=tmp[5]:
            gene.append(flag)
            length.append(sumlen)
            sumlen = 0
        flag = tmp[5]
        sumlen += int(tmp[2])-int(tmp[1])
    gene.append(flag)
    length.append(sumlen)
ll = pd.DataFrame({'gene':gene,'length':length},columns=['gene', 'length'])

total = mydat['count'].sum()
Q75l = ll.quantile(q=0.75)[0]

gene_e = pd.merge(mydat,ll, on='gene')
gene_e['FPKM']=gene_e['count']*1000000000/gene_e['length']/total
gene_e['FPKM-UQ']=gene_e['count']*1000000000/gene_e['length']/Q75l
# gene_e.round(decimals=5)
# pandas 0.17 add,
gene_e['FPKM'] = gene_e['FPKM'].map('{:.5f}'.format)
gene_e['FPKM-UQ'] = gene_e['FPKM-UQ'].map('{:.5f}'.format)
gene_e.to_csv(sys.argv[3],sep="\t",index=False)