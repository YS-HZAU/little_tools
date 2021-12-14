# 比对类工具
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