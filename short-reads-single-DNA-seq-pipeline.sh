thread=4
indir=data
index=/public/home/xyhuang/zhangyan/genome/hg38.analysisSet.chroms/hg38.fa
species=human
GENOME_LEN=2913022398 # perl -lane '{$_=~s/[Nn]+//g;$sum+=length($_);}END{print $sum;}' hg38.fa 未考虑repeat的影响，但是如果所有的都设置一样的话就没有影响了。
for i in ENCFF000RMI
do
# qc
mkdir -p qcdir
bsub -q q2680v2 -J qc -n $thread -o qc.out -e qc.err -R span[hosts=1] " fastqc -t $thread -o qcdir $indir/${i}.fastq.gz "

# 正常情况下，chip-seq的建库都是Illumina Universal Adapter接头，参数不需要做修改。
# ATAC-seq建库都有Tn5序列（Nextera Transposase Sequence）
# qc control
mkdir -p trim
# ATAC-seq
bsub -q q2680v2 -J trim -n $thread -o trim.out -e trim.err -R span[hosts=1] " java -jar /public/home/xyhuang/Tools/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads $thread -phred33 $indir/${i}.fastq.gz trim/${i}.fq.gz ILLUMINACLIP:adapter.fa:2:30:7:8:true LEADING:5 TRAILING:5 SLIDINGWINDOW:4:15 MINLEN:30 && fastqc -t $thread trim/$i.fq.gz "
# ChIP-seq and WGS/WES/WXS
bsub -q q2680v2 -J trim -n $thread -o trim.out -e trim.err -R span[hosts=1] " java -jar /public/home/xyhuang/Tools/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads $thread -phred33 $indir/${i}.fastq.gz trim/${i}.fq.gz ILLUMINACLIP:/public/home/xyhuang/Tools/Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:7:8:true LEADING:3 TRAILING:3 AVGQUAL:20 SLIDINGWINDOW:4:15 MINLEN:30 && fastqc -t $thread trim/$i.fq.gz "
bsub -q q2680v2 -J trim -n 1 -o trim.out -e trim.err -R span[hosts=1] " python /public/home/xyhuang/longread_pipeline/longread_pipeline/program/remove_duplicated_reads_SE.py trim/$i.fq.gz trim/$i.uniq.fq.gz && fastqc -t 1 trim/$i.uniq.fq.gz "

# align
mkdir -p aligndir
bsub -q q2680v2 -J align -n $thread -o align.out -e align.err -R span[hosts=1] " bwa aln -t $thread -f aligndir/$i.sai $index trim/$i.uniq.fq.gz && bwa samse -r \"@RG\\tID:$i\\tSM:$i\\tLB:$species\\tPL:illumina\\tPU:run\" $index aligndir/$i.sai trim/$i.uniq.fq.gz | samtools view -Sb - | samtools sort -@ $thread -o aligndir/$i.bam - "

# filter
module load R/3.5.2bsub -q q2680v2 -J rmdup -n 1 -o rmdup.out -e rmdup.err -R span[hosts=1] " python /public/home/xyhuang/Tools/littletools/UniqFileBam.py -t bwa-aln -i aligndir/${i}.bam -o aligndir/${i}.flt.bam -q 20 && samtools index aligndir/${i}.flt.bam && samtools flagstat aligndir/${i}.bam > aligndir/${i}.bam.stat && samtools flagstat aligndir/${i}.flt.bam > aligndir/${i}.flt.bam.stat && samtools view -o aligndir/${i}.flt.rm.bam aligndir/${i}.flt.bam chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11 chr12 chr13 chr14 chr15 chr16 chr17 chr18 chr19 chr20 chr21 chr22 chrX chrY && samtools index aligndir/${i}.flt.rm.bam && samtools flagstat aligndir/${i}.flt.rm.bam > aligndir/${i}.flt.rm.bam.stat && Rscript /public/home/xyhuang/Tools/phantompeakqualtools/run_spp.R  -c=aligndir/${i}.flt.rm.bam -savp=aligndir/${i}.flt.rm.bam.spp.pdf -out=aligndir/${i}.flt.rm.bam.spp.txt > aligndir/${i}.flt.rm.bam.richtest.log && Rscript /public/home/xyhuang/Tools/phantompeakqualtools/run_spp.R  -c=aligndir/${i}.flt.bam -savp=aligndir/${i}.flt.bam.spp.pdf -out=aligndir/${i}.flt.bam.spp.txt > aligndir/${i}.flt.bam.richtest.log "

# bam2bw and callpeak
bsub -J bam2bw -n $thread -o bam2bw.out -e bam2bw.err -R span[hosts=1] "bamCoverage -o aligndir/$i.RPKM.bw --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 --normalizeUsing RPKM && bamCoverage -o aligndir/$i.bw --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 && bamCoverage -o aligndir/$i.1x.bw --binSize 5 -b aligndir/$i.flt.bam --numberOfProcessors $thread --minMappingQuality 20 --normalizeUsing RPGC --effectiveGenomeSize $GENOME_LEN "
mkdir -p peak
bsub -q q2680v2 -J peakcalling -n 1 -o peakcalling.out -e peakcalling.err -R span[hosts=1] " macs2 callpeak -t aligndir/$i.flt.bam -c /public/home/xyhuang/zhangyan/ChIPSeq/A549.control/aligndir/ENCFF000RMI.flt.bam -f BAM -g $GENOME_LEN -n peak/$i.narrow --trackline -B --verbose 3 --SPMR --keep-dup all && macs2 callpeak -t aligndir/$i.flt.bam -c /public/home/xyhuang/zhangyan/ChIPSeq/A549.control/aligndir/ENCFF000RMI.flt.bam -f BAM -g $GENOME_LEN -n peak/$i.broad --trackline -B --verbose 3 --SPMR --broad --keep-dup all "

done


# peak merge
bsub -q q2680v2 -J peakmerge -n 1 -o peakmerge.out -e peakmerge.err -R span[hosts=1] " idr --samples peak/ENCFF000RMB.narrow_peaks.narrowPeak peak/ENCFF000RMC.narrow_peaks.narrowPeak --input-file-type narrowPeak --output-file peak/A549.CTCF.idrValues.peak --output-file-type narrowPeak --plot peak/A549.CTCF.idrValues.peak.png --verbose "
bsub -q q2680v2 -J peakmerge -n 1 -o peakmerge.out -e peakmerge.err -R span[hosts=1] " idr --samples peak/ENCFF000RMM.broad_peaks.broadPeak peak/ENCFF000RMO.broad_peaks.broadPeak --input-file-type broadPeak --output-file peak/A549.RNAPII.idrValues.peak --output-file-type broadPeak --plot peak/A549.RNAPII.idrValues.peak.png --verbose "



# cat adapter.fa
>seq1
CTGTCTCTTATACACATCTGACGCTGCCGACGA
>seq2
CTGTCTCTTATACACATCTCCGAGCCCACGAGAC