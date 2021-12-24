# 文献检索
[scihub](https://www.scihub.net.cn/)<br/>

# RNA 数据库条目
### snoRNA/snRNA database
刚开始的时候，snoRNA和snRNA没有明显的差别，可以看到很多早期文献还在称U3为snRNA。所以合并了snRNA/snoRNA。<br/>
[酵母的snoRNA数据库](https://people.biochem.umass.edu/fournierlab/snornadb/mastertable.php)<br/>
[人的snoRNA数据库](https://www-snorna.biotoul.fr/getseq.php)。可以从这个网站下载snoRNA的序列。

### ncRNA(有冗余分类)
[GREAT](http://great.stanford.edu/public/html/)，根据附近的基因的注释，对非编码基因区域进行生物学意义注释。<br/>
[AnnoLnc2](http://annolnc.gao-lab.org/index.php)。人和小鼠lncRNA的注释，包括lncRNA预测，相关miRNA，保守性，二级结构，GO注释等等。[使用 RepeatMasker 来预测的序列当中是否有重复序列; 通过ViennaRNA (http://rna.tbi.univie.ac.at/) 数据库来预测lncRNA的二级结构；数据库使用了GETx数据库里面的正常组织、CCLE里面的癌症细胞系以及ENCODE数据库里面的数据来进行查看基因的表达情况；通过比较核/胞质表达来确定这个lncRNA主要是在哪个地方表达；使用GTRD来预测lncRNA的可能收到的转录因子调控作用，同时使用TargetScan来预测其miRNA调控的作用；通过GWAS数据库来寻找影响这个lncRNA的SNP，进一步的通过eQTL来评价哪些SNP对于这个lncRNA的表达有影响，这个分析的主要数据来自于GETx；由于使用的RNA-seq的数据，所以就可以看lncRNA的表达和哪些基因存在共表达关系；使用了目前发表的GEO上面的CLIP-seq的数据来进行分析，对于GEO里面没有的蛋白数据，数据库使用lncPro数据库来进行预测。所以在结果当中就包括两个部分，一个是lncPro数据库的结果，另外一个则是CLIP-seq分析的结果；预测这个lncRNA的功能了。由于lncRNA本身是不会编码蛋白来发挥作用的，所以主要是通过其相互作用的基因来预测这个lncRNA的功能，这个数据库主要预测了lncRNA本身GO分析的功能；通过phyloFit来比较物种之间的进化关系](https://www.sci666.com.cn/66870.html)

# RNA 二级结构
[RNArchitecture](http://genesilico.pl/RNArchitecture/family/MIR807/secondarystructure)

# repeat 数据库条目（有些repeat RNA也属于该条目）
### repeat database
[RepBase](https://www.girinst.org/server/RepBase/)是一个整理的repeat数据库，但是使用需要支付昂贵的费用。在repeatmasker网站上公开了两个版本的[RepBase](http://repeatmasker.org/libraries/)：RepBaseRepeatMaskerEdition-20181026.tar.gz和RepeatMaskerMetaData-20170127.tar.gz。<br/>
[Dfam](https://www.dfam.org/home), [Transposable Element DNA sequence alignments, hidden Markov Models (HMMs)](https://www.dfam.org/releases/Dfam_3.5/annotations/hg38/)<br/>
### repeatmask注释条目
[RMGenomicDatasets](http://www.repeatmasker.org/genomicDatasets/RMGenomicDatasets.html)年代久远而且和UCSC下载的对不上。UCSC的用的是20130422版。
[repeatmask的说明](http://www.repeatmasker.org/faq.html)

# genome & annotation 数据库条目
### 水稻基因组
[ZS97 & MH63](https://rice.hzau.edu.cn/cgi-bin/rice_rs3/download_ext)，缺点是不含线粒体和叶绿体<br/>
[日本晴 Oryza](https://rapdb.dna.affrc.go.jp/download/irgsp1.html)，含有线粒体，叶绿体<br/>
[UCSC基因组来源](http://genome.ucsc.edu/goldenPath/credits.html)<br/>
[USCS收录的人类基因组注释](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/)，以及一个[更新版](http://hgdownload.soe.ucsc.edu/goldenPath/archive/hg38/)<br/>
[human基因注释和功能注释 genecards](https://www.genecards.org/)<br/>
[human基因注释和功能注释 HGNC](https://www.genenames.org/)<br/>

# 常用在线小工具
### 比对
[多序列比对](https://www.novopro.cn/tools/muscle.html)<br/>
[DeepL翻译器](https://www.deepl.com/translator)<br/>
[科研者之家](https://www.home-for-researchers.com/static/index.html#/)<br/>
InterProscan 输出格式
```
1. 蛋白质接入号	Protein Accession (e.g. P51587)
2. 序列的 MD5 值	Sequence MD5 digest (e.g. 14086411a2cdf1c4cba63020e1622579)
3. 序列长度	Sequence Length (e.g. 3418)
4. 不同分析方案	Analysis (e.g. Pfam / PRINTS / Gene3D)
5. 签名号	Signature Accession (e.g. PF09103 / G3DSA:2.40.50.140)
6. 签名描述	Signature Description (e.g. BRCA2 repeat profile)
7. 起始位置	Start location
8. 终止位置	Stop location
9. 得分	Score - is the e-value (or score) of the match reported by member database method (e.g. 3.1E-52)
10. 状态	Status - is the status of the match (T: true)
11. 运行日期	Date - is the date of the run
12... 其他 	(InterPro annotations - accession (e.g. IPR002093) - optional column; only displayed if -iprlookup option is switched on)
	(InterPro annotations - description (e.g. BRCA2 repeat) - optional column; only displayed if -iprlookup option is switched on)
	(GO annotations (e.g. GO:0005515) - optional column; only displayed if --goterms option is switched on)
	(Pathways annotations (e.g. REACT_71) - optional column; only displayed if --pathways option is switched on)
```
# 林奈分类以及一些常见简写

简写 | 全称 | 翻译 | 发现的场景
----|----|----|----
CB  | Caenorhabditis briggsae | 广杆属线虫 | repbase中查阅
ECa | Eucalyptus camaldulensis| 赤桉; 桉树林多为赤桉 | repbase中查阅
EC  | Equus caballus | 马 | repbase中查阅（少量）
ML  | Myotis lucifugus|蝙蝠|repbase中查阅
CR  | Chlamydomonas reinhardtii | 莱茵衣藻 | repbase中查阅
SP  | Strongylocentrotus | 海胆 | repbase中查阅