import sys
from collections import OrderedDict

'''
perl -lane 'if($F[2]eq"gene"){if(/gene_id "(.+?)\.\d+";.+?gene_name "(.+?)";/){$st=$F[3]-1;print "$F[0]\t$st\t$F[4]\t$1\t.\t$F[6]\t$2"}}' ~/zhangyan/genome/gencode.v24.annotation.gtf > hg38.bed
sort -k1,1 -k2,2n -k3,3n hg38.bed | awk -v OFS="\t" '{$7=$4"-genebody";print $0}' > hg38.genebody.bed
awk -v OFS="\t" '{if($6=="+"){start=$2-2000;if(start<0){start=0;}print $1,start,$2+2000,$4,$5,$6,$4"-promoter"}else{start=$3-2000;if(start<0){start=0;}print $1,start,$3+2000,$4,$5,$6,$4"-promoter"}}' hg38.bed | sort -k1,1 -k2,2n -k3,3n > hg38.promoter.bed
awk -v OFS="\t" '{if($6=="+"){start=$3-2000;if(start<0){start=0;}print $1,start,$3+2000,$4,$5,$6,$4"-terminal"}else{start=$2-2000;if(start<0){start=0;}print $1,start,$2+2000,$4,$5,$6,$4"-terminal"}}' hg38.bed | sort -k1,1 -k2,2n -k3,3n > hg38.terminal.bed
perl -lane 'if($F[2]eq"exon"){if(/gene_id "(.+?)\.\d+";.+?transcript_id "(.+?)\.\d+";.+?exon_number (\d+);/){$st=$F[3]-1;print "$F[0]\t$st\t$F[4]\t$1\t.\t$F[6]\t$2-exon-$3"}}' ~/zhangyan/genome/gencode.v24.annotation.gtf | sort -k1,1 -k2,2n -k3,3n > hg38.exon.bed

bedtools intersect -a peak/allrich-06.DNA_peaks.narrowPeak -b /public/home/xyhuang/zhangyan/ChRDSeq/hg38.genebody.bed -wao > peak/allrich-06.DNA.genebody.overlap.bed
bedtools intersect -a peak/allrich-06.DNA_peaks.narrowPeak -b /public/home/xyhuang/zhangyan/ChRDSeq/hg38.promoter.bed -wao > peak/allrich-06.DNA.promoter.overlap.bed
bedtools intersect -a peak/allrich-06.DNA_peaks.narrowPeak -b /public/home/xyhuang/zhangyan/ChRDSeq/hg38.terminal.bed -wao > peak/allrich-06.DNA.terminal.overlap.bed
bedtools intersect -a peak/allrich-06.DNA_peaks.narrowPeak -b /public/home/xyhuang/zhangyan/ChRDSeq/hg38.exon.bed -wao > peak/allrich-06.DNA.exon.overlap.bed

python annopeak.py peak/allrich-06.DNA.promoter.overlap.bed peak/allrich-06.DNA.genebody.overlap.bed peak/allrich-06.DNA.exon.overlap.bed peak/allrich-06.DNA.terminal.overlap.bed > peak/allrich-06.DNA.anno.result.txt
'''

anno = OrderedDict()
with open(sys.argv[1],'r') as promoter , open(sys.argv[2],'r') as body , open(sys.argv[3],'r') as exon , open(sys.argv[4],'r') as terminal:
    flag = None
    outlist = []
    n = 0
    for line in promoter:
        tmp = line.strip().split("\t")
        n = len(tmp) - 8
        uid = "\t".join(tmp[0:n])
        if flag != None and flag != uid:
            anno[flag] = {}
            anno[flag]['promoter'] = set(outlist)
            outlist = []
        flag = uid
        outlist.append(tmp[n+3]+","+tmp[n+6])
    anno[flag] = {}
    anno[flag]['promoter'] = set(outlist)

    flag = None
    outlist = []
    for line in body:
        tmp = line.strip().split("\t")
        uid = "\t".join(tmp[0:n])
        if flag != None and flag != uid:
            anno[flag]['body'] = set(outlist)
            outlist = []
        flag = uid
        outlist.append(tmp[n+3]+","+tmp[n+6])
    anno[flag]['body'] = set(outlist)

    flag = None
    outlist = []
    for line in exon:
        tmp = line.strip().split("\t")
        uid = "\t".join(tmp[0:n])
        if flag != None and flag != uid:
            anno[flag]['exon'] = set(outlist)
            outlist = []
        flag = uid
        outlist.append(tmp[n+3]+","+tmp[n+6])
    anno[flag]['exon'] = set(outlist)

    flag = None
    outlist = []
    for line in terminal:
        tmp = line.strip().split("\t")
        uid = "\t".join(tmp[0:n])
        if flag != None and flag != uid:
            anno[flag]['terminal'] = set(outlist)
            outlist = []
        flag = uid
        outlist.append(tmp[n+3]+","+tmp[n+6])
    anno[flag]['terminal'] = set(outlist)

for i in anno.keys():
    if ".,." in anno[i]['promoter'] and ".,." in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'intergenic',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'up-promoter',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'intron-promoter',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." not in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'exon-promoter',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." not in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'exon',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." in anno[i]['terminal']:
        print(i,'intron',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'intron-terminal',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." not in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'exon-terminal',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." in anno[i]['promoter'] and ".,." in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'down-terminal',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'overlapp',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." not in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'exon-intron-overlapp',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." not in anno[i]['body'] and ".,." in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'intron-overlapp',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    elif ".,." not in anno[i]['promoter'] and ".,." in anno[i]['body'] and ".,." not in anno[i]['exon'] and ".,." not in anno[i]['terminal']:
        print(i,'exon-overlapp',";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")
    else:
        print('error',i,";".join(anno[i]['promoter']),";".join(anno[i]['body']),";".join(anno[i]['exon']),";".join(anno[i]['terminal']),sep="\t")