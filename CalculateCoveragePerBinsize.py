"""
将基因组分bin，然后统计落在每个bin中的数量(bed文件取中间点)。生成bedgraph格式的输出
python calculatorCov.py bins.bed 1000000 input.bed output.bedgraph
hg38.fa.fai：samtools faidx hg38.fa
hg38.size：cut -f 1-2 hg38.fa.fai > hg38.size
bins.bed：bedtools makewindows -g hg38.size -w 1000000 -s 1000000 | awk -v OFS="\t" '{{print $0,NR}}' > bins.bed
1000000：步长
"""
import sys

def main(bins,length,infile,outfile):
    # load bed file
    beddict = {} # beddict -> chrom -> pos -> count
    with open(bins,'r') as fin:
        for line in fin:
            tmp = line.strip().split()
            if tmp[0] not in beddict:
                beddict[tmp[0]] = {}
            beddict[tmp[0]][int(tmp[1])] = 0
    # print(beddict)

    # load input file and calculator the coverage
    length = int(length)
    with open(infile,'r') as fin:
        for line in fin:
            tmp = line.strip().split()
            pos = int((int(tmp[1])+int(tmp[2]))/2/length)*length
            beddict[tmp[0]][pos] += 1
    
    # print result to output file
    with open(bins,'r') as fin,open(outfile,'w') as fout:
        for line in fin:
            tmp = line.strip().split()
            fout.write(tmp[0]+"\t"+tmp[1]+"\t"+tmp[2]+"\t"+str(beddict[tmp[0]][int(tmp[1])])+"\n")

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])