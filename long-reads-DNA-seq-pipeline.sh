thread=4
indir=data
index=/public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/hg38.fa
species=human
GENOME_LEN=2913022398 # perl -lane '{$_=~s/[Nn]+//g;$sum+=length($_);}END{print $sum;}' hg38.fa 未考虑repeat的影响，但是如果所有的都设置一样的话就没有影响了。
for i in hch-04 hch-05
do

# qc
mkdir -p qcdir
bsub -q q2680v2 -J qc -n $thread -o qc.out -e qc.err -R span[hosts=1] " fastqc -t $thread -o qcdir $indir/${i}_R1.fq.gz $indir/${i}_R2.fq.gz "

# qc control
mkdir -p trim
bsub -q q2680v2 -J trim -n $thread -o trim.out -e trim.err -R span[hosts=1] " java -jar /public/home/xyhuang/Tools/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads $thread -phred33 data/${i}_R1.fq.gz data/${i}_R2.fq.gz trim/${i}_R1.fq.gz trim/${i}_R1.un.fq.gz trim/${i}_R2.fq.gz trim/${i}_R2.un.fq.gz ILLUMINACLIP:/public/home/xyhuang/Tools/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:7:8:true LEADING:10 TRAILING:10 AVGQUAL:20 SLIDINGWINDOW:4:15 MINLEN:50 "
bsub -q q2680v2 -J trim -n 2 -o trim.out -e trim.err -R span[hosts=1] " python /public/home/xyhuang/longread_pipeline/longread_pipeline/program/remove_duplicated_reads.py trim/${i}_R1.fq.gz trim/${i}_R2.fq.gz trim/${i}_R1.uniq.fq.gz trim/${i}_R2.uniq.fq.gz && fastqc -t 2 trim/${i}_R1.uniq.fq.gz trim/${i}_R2.uniq.fq.gz "

# align
mkdir -p aligndir
bsub -q q2680v2 -J align -n $thread -o align.out -e align.err -R span[hosts=1] " bwa mem -t $thread $index trim/${i}_R1.uniq.fq.gz trim/${i}_R2.uniq.fq.gz -R \"@RG\\tID:$i\\tSM:$i\\tLB:$species\\tPL:illumina\\tPU:run\" | samtools view -Sb - | samtools sort -@ $thread -o aligndir/$i.bam - && samtools index aligndir/$i.bam "

# filter
module load R/3.5.2
bsub -q q2680v2 -J filter -n 1 -o filter.out -e filter.err -R span[hosts=1] " java -jar /public/home/xyhuang/Tools/javatools/picard.jar CollectInsertSizeMetrics I=aligndir/${i}.bam O=aligndir/${i}.insert_size_metrics.txt H=aligndir/${i}.insert_size_histogram.pdf M=0.5 VALIDATION_STRINGENCY=SILENT && python /public/home/xyhuang/Tools/littletools/UniqFileBam.py -t bwa-mem -i aligndir/${i}.bam -o aligndir/${i}.flt.bam -q 20 && samtools index aligndir/${i}.flt.bam && samtools flagstat aligndir/${i}.bam > aligndir/${i}.bam.stat && samtools flagstat aligndir/${i}.flt.bam > aligndir/${i}.flt.bam.stat && samtools view -o aligndir/${i}.flt.rm.bam aligndir/${i}.flt.bam chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11 chr12 chr13 chr14 chr15 chr16 chr17 chr18 chr19 chr20 chr21 chr22 chrX chrY && samtools index aligndir/${i}.flt.rm.bam && samtools flagstat aligndir/${i}.flt.rm.bam > aligndir/${i}.flt.rm.bam.stat && Rscript /public/home/xyhuang/Tools/phantompeakqualtools/run_spp.R  -c=aligndir/${i}.flt.rm.bam -savp=aligndir/${i}.flt.rm.bam.spp.pdf -out=aligndir/${i}.flt.rm.bam.spp.txt > aligndir/${i}.flt.rm.bam.richtest.log && Rscript /public/home/xyhuang/Tools/phantompeakqualtools/run_spp.R  -c=aligndir/${i}.flt.bam -savp=aligndir/${i}.flt.bam.spp.pdf -out=aligndir/${i}.flt.bam.spp.txt > aligndir/${i}.flt.bam.richtest.log "