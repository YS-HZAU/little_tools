thread=10
indir=data
index=/public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/hg38
knownspl=/public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/genome.ss
species=human
GENOME_LEN=2913022398 # perl -lane '{$_=~s/[Nn]+//g;$sum+=length($_);}END{print $sum;}' hg38.fa 未考虑repeat的影响，但是如果所有的都设置一样的话就没有影响了。
for i in totalRS-01 totalRS-02
do
# qc
mkdir -p qcdir
bsub -q q2680v2 -J qc -n $thread -o qc.out -e qc.err -R span[hosts=1] " fastqc -t $thread -o qcdir $indir/${i}_R1.fq.gz $indir/${i}_R2.fq.gz "

# 正常情况下，RNA-seq的建库都是Illumina Universal Adapter接头，参数不需要做修改。
# qc control
mkdir -p trim
bsub -q q2680v2 -J trim -n $thread -o trim.out -e trim.err -R span[hosts=1] " java -jar ~/Tools/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads 4 data/${i}_R1.fq.gz data/${i}_R2.fq.gz trim/${i}_R1.fq.gz trim/${i}_R1.un.fq.gz trim/${i}_R2.fq.gz trim/${i}_R2.un.fq.gz ILLUMINACLIP:/public/home/xyhuang/Tools/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:7:8:true LEADING:25 TRAILING:20 SLIDINGWINDOW:4:15 MINLEN:30 && fastqc -t $thread trim/${i}_R1.fq.gz trim/${i}_R2.fq.gz"

# 目前的连特异性建库几乎都是RF参数的。非连特异性建库的请去掉该参数
# hisat2 -x /public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/hg38 -1 trim/totalRS-01_R1.fq.gz -2 trim/totalRS-01_R2.fq.gz | head -2000000 > totalRS-01.test.sam
# infer_experiment.py -i totalRS-01.test.sam -r /public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/hg38.gene.bed12 -s 800000 > totalRS-01.test.sam.strand # RSeQC可以判断。
# align
mkdir -p aligndir
bsub -q q2680v2 -J align -n $thread -o align.out -e align.err -R span[hosts=1] " hisat2 --known-splicesite-infile $knownspl --rna-strandness RF --rg-id \"$i\" --rg LB:total --rg PG:hisat2  --rg PL:ILLUMINA --rg PU:lane --rg SM:$i -p $thread -x $index -1 trim/${i}_R1.fq.gz -2 trim/${i}_R2.fq.gz | tee aligndir/$i.sam | samtools view -Sb - | samtools sort -@ $thread -o aligndir/$i.bam - "

# count
bsub -q q2680v2 -J count.run -n 1 -o count.run.out -e count.run.err -R span[hosts=1] " htseq-count -s reverse -f sam -r name aligndir/$i.sam /public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/gencode.v35.annotation.gtf > aligndir/$i.RNA.count && gzip aligndir/$i.sam "

# filtering data
module load R/3.5.2
bsub -q q2680v2 -J flt -n 1 -o flt.out -e flt.err -R span[hosts=1] " python /public/home/xyhuang/Tools/littletools/UniqFileBamAsPair.py -t hisat -i aligndir/${i}.bam -o aligndir/${i}.flt.bam -q 20 && java -jar /public/home/xyhuang/Tools/javatools/picard.jar CollectInsertSizeMetrics I=aligndir/${i}.flt.bam O=aligndir/${i}.insert_size_metrics.txt H=aligndir/${i}.insert_size_histogram.pdf M=0.5 VALIDATION_STRINGENCY=SILENT && samtools index aligndir/${i}.flt.bam && samtools flagstat aligndir/${i}.bam > aligndir/${i}.bam.stat && samtools flagstat aligndir/${i}.flt.bam > aligndir/${i}.flt.bam.stat "

# bam2bw
bsub -q q2680v2  -J bam2bw -n $thread -o bam2bw.out -e bam2bw.err -R span[hosts=1] " bamCoverage -o aligndir/$i.RPKM.bw --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 --normalizeUsing RPKM && bamCoverage -o aligndir/$i.bw --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 && bamCoverage -o aligndir/$i.fwd.RPKM.bw --filterRNAstrand forward --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 --normalizeUsing RPKM && bamCoverage -o aligndir/$i.fwd.bw --filterRNAstrand forward --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 && bamCoverage -o aligndir/$i.rev.RPKM.bw --filterRNAstrand reverse --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 --normalizeUsing RPKM && bamCoverage -o aligndir/$i.rev.bw --filterRNAstrand reverse --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 "