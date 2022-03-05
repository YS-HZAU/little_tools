# 比对类工具
### 关于比对类工具处理兼并碱基
可以下载[水稻的细胞器基因组](https://rapdb.dna.affrc.go.jp/download/archive/Mt_Pt_genome.fasta)文件，里面包含了兼并碱基，也可以自定义。下载后，提取了一段reads做如下操作
```
@test1
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCARCCC
+
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCARCCC
@test2
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCAACCC
+
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCAACCC
@test3
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCAGCCC
+
ATTGGCGGGAGTATATTATGGCAGGATCAGTCACCTGGGCAAACCAGCCC

bwa：
bwa index Mt_Pt_genome.fasta
bwa mem Mt_Pt_genome.fasta test.fq

hisat2:
hisat2-build Mt_Pt_genome.fasta Mt_Pt_genome
hisat2 -x Mt_Pt_genome -U test.fq

STAR:
mkdir -p starindex && STAR --runMode genomeGenerate --genomeDir starindex --genomeFastaFiles Mt_Pt_genome.fasta
STAR --genomeDir starindex/ --outFileNamePrefix startest --readFilesIn test.fq 
```
bwa的结果如图
![](figformanual\bwa.png)
将fastq文件中的兼并碱基变成了N。同时，基因组索引文件中，这个位置被记录成了G
hisat2的结果如图
![](figformanual\hisat2.png)
将fastq文件中的兼并碱基变成了A。而在基因组索引文件中，该位置被记录成N了。
STAR的结果如图
![](figformanual\STAR.png)
三个均无错配，说明可以识别兼并碱基
### blast
HAL1序列来源于RepBaseRepeatMaskerEdition-20181026.tar.gz，与[hg38 repeat](http://www.repeatmasker.org/genomes/hg38/RepeatMasker-rm405-db20140131/hg38.fa.out.gz)作比较。结果发现blast的比对结果短于注释的结果（bwa比对上的结果远远短于）。
```
makeblastdb -in hg38.fa -input_type fasta -dbtype nucl -parse_seqids -out hg38.blast.db -logfile hg38.log.txt
blastn -query HAL1.fa -out HAL1.blast.output -db hg38.blast.db -outfmt 6 -evalue 1e-5 -max_target_seqs 1000
```
输出文件说明
```
HAL1	chr12	74.464	979	172	43	1196	2153	49009079	49008158	1.40e-96	361
qacc：待比对的序列ID
sacc：比对上的ID
pident：相同匹配的百分比
length：比对上的长度
mismatch：错配数量
gapopen：缺口数量
qstart：待比对的序列起点
qend：待比对的序列终点
sstart：比对上的序列起点
send：比对上的序列终点
evalue：Expect value
bitscore：得分

# 亦可从下面选择任意自定义
qseqid qlen sseqid sgi slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxid ssciname
```
### bwa
aln:
```
XT:U => Unique alignment
XT:R => Repeat
XT:N => Not mapped
XT:M => Mate-sw (成对比对的时候，当一端是被另一端救援而被确定比对位置的时候)
```

# 定量工具
### featureCounts
[subread for featureCounts](https://github.com/DeskGen/subread).<br/>
可以对多位点比对的reads按百分数处理。单端数据：(针对RNA数据，因为一个reads只能有一个rna的来源，所以主要参数是--fraction -M)
```
featureCounts -a chr21.gtf -o chr21feature -t gene --largestOverlap --fraction -M -s 1  -J -G ~/Genome/GRCh3885/hg38.fa --donotsort -T 4 -R SAM --Rpath outtest/ --verbose -g gene_id chr21.bam

--fraction -M/-O ：平均分配多位点比对的结果
-g ：注意有些注释文件中可能不是gene_id，需要用-g修改

# 单端数据
featureCounts -a hg38.remove.gtf -o featureCounts.2.exon.txt -t exon -g gene_id -s 2 -R BAM -T 1 --Rpath exon2featureCounts --verbose uniqsplitfile/allrich-06.uniqmap.tmp.1.bam 

# 双端命令
featureCounts -a gencode_v26_Subread_to_DEXSeq.gtf -o SRR1797250.gene.count -t exon -g gene_id -p -T 1 SRR1797250.bam  
-p 将结果当成fragment来处理
-B 是不是双端都需要比对上(htseq默认是)
-P -d -D 设置插入片段大小
-C 不计算两端唯一不同染色体和位于同一染色体但链方向不一致的reads。
--donotsort 和htseq一样，都需要输入文件按name排序，不要相信提供的pos排序的参数。
--largestOverlap 分配给最长的比对的结果。

featureCounts -a ~/zhangyan/genome/hg38.analysisSet.chroms/hg38.remove.gtf -o featureCounts.${i}.${j}.txt -t ${j} -g gene_id -s ${i} -R BAM -T 1 --Rpath ${j}.${i}.featureCounts --verbose allrich-23.uniqmap.tmp.1.bam
featureCounts -a ~/zhangyan/genome/hg38.analysisSet.chroms/hg38.remove.gtf -o featureCounts.${i}.${j}.longest.txt -t ${j} -g gene_id --largestOverlap -s ${i} -R BAM -T 1 --Rpath ${j}.${i}.featureCounts.longest --verbose allrich-23.uniqmap.tmp.1.bam
```

# 序列拼接工具
### flash
[flash](http://ccb.jhu.edu/software/FLASH/index.shtml)
```
flash -M 150 -O --threads 12 --output-prefix out.flash --output-directory . read1.clean.fq read2.clean.fq
```
bug: 无法处理R1（R2）完全包含的reads。可能因为测序的偏差，导致R1和R2中的一段reads测序质量低被过滤掉。但是flash无法处理该情况。同时该情况在pandaseq中依然存在，而且pandaseq会输出一个明显错误的结果，flash输出为不拼接的结果。
```
R1: GTGAGCTGCCTTGGAAAAGGTTTGACATCATGGTCTCACCCTCCAGGCATTCGCAATGCTGTTGAAGCACTCTGGGCAATTCGGCTGGATTGCAACAGCCTCCTCGTTCTTCGCGATGCACATGTCAAACTCTCGTAGCTAAACCAAATC
R2: 
ATTTGGTTTAGCTACGAGAGGTTGACATGTGCATCGCGAAGAACGAGGAGGCTGTTGCAATCCAGCCGAATTGCCCAGAGTGCTTCAACAGCATTGCGAATGCCTGGAGGGTGAGACCATGATGTCAAACCTTTTCCAAGGC

R1: GTGAGCTGCCTTGGAAAAGGTTTGACATCATGGTCTCACCCTCCAGGCATTCGCAATGCTGTTGAAGCACTCTGGGCAATTCGGCTGGATTGCAACAGCCTCCTCGTTCTTCGCGATGCACATGTCAACCTCTCGTAGCTAAACCAAATC
R2: 
ATTTGGTTTAGCTACGAGAGGTTGACATGTGCATCGCGAAGAACGAGGAGGCTGTTGCAATCCAGCCGAATTGCCCAGAGTGCTTCAACAGCATTGCGAATGCCTGGAGGGTGAGACCATGATGTCAAACCTTTTCCAAGGC
```

# 变异
### 变异注释
[网页学习链接Annovar，SnpEff，Oncotator](http://yangli.name/2016/05/15/20160515annotation/)

# 注释
### 转录组注释
[InterProscan](http://www.ebi.ac.uk/interpro/download/)，[GitHub](https://github.com/ebi-pf-team/interproscan)
```
module load interproscan/5.48-83.0 && interproscan.sh --appl Pfam -t n -dp -i Pfam/dir${i}/part.${i}.fa --iprlookup -f tsv -o Pfam/dir${i}/part.${i}.fa.interproscan -cpu 5 -goterms -pa
可以移除参数--appl Pfam，对所有的数据库进行注释，默认是对蛋白序列，-t n修改为DNA/RNA核苷酸序列
```

# Linux
### sort （Linux常用命令）
看起来sort是忽略了字母大小写排序，目前还没仔细研究，日后再仔细研究。现在碰到sort请全部用LANG=C sort来代替。运行速度更快，跟其它软件sort之后的结果一致。
```
echo -e "snoR1\nSNOR75\nsnoR1\nsnoR75" > test
sort test 
    snoR1
    snoR1
    snoR75
    SNOR75

LANG=C sort test
    SNOR75
    snoR1
    snoR1
    snoR75
```

# 统计学
### 变异系数（CV）
1：标准差与平均数的比值称为变异系数，记为C·V。
2：变异系数可以消除单位和（或）平均数不同对两个或多个资料变异程度比较的影响。
```
aa = c(5.8,4.6,4.9)
sd(aa)/mean(aa)
```