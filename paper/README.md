# 参考文献
### 无连接三维基因组测序
[SPRITE](https://www.cell.com/cell/fulltext/S0092-8674(18)30636-6?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867418306366%3Fshowall%3Dtrue).[Higher-Order Inter-chromosomal Hubs Shape 3D Genome Organization in the Nucleus](https://doi.org/10.1016/j.cell.2018.05.024).<br/>
- 在反应池中给蛋白-DNA复合物上的DNA序列上连接上特别设计的barcode序列。用这个barcode序列来标记一个个的DNA复合物。默认是同一个标记的DNA是在空间上靠近的。
- 分析中AB compartment用的[cworld](https://github.com/dekkerlab/cworld-dekker)，TAD用的[matrix2insulation.pl](https://github.com/dekkerlab/crane-nature-2015/tree/master/scripts)，Loop用的和juicer一样的方法（自己开发）。可能还是存在数据量不够的问题，尝试用juicer做AB compartment，TAD，Loop不能得到好结果

### 三维基因组测序
[第一篇HiC技术报道文献](https://www.science.org/doi/10.1126/science.1181369). [Comprehensive Mapping of Long-Range Interactions Reveals Folding Principles of the Human Genome](DOI: 10.1126/science.1181369)
- 第一篇提出HiC技术的文章

[第一篇提出TAD概念](https://www.nature.com/articles/nature11082). [Topological domains in mammalian genomes identified by analysis of chromatin interactions](doi:10.1038/nature11082)
- TAD分析

[X染色体失活](https://www.nature.com/articles/nature11049). [Spatial partitioning of the regulatory landscape of the X-inactivation centre](doi:10.1038/nature11049)
- X失活

[insitu HiC](https://www.cell.com/cell/fulltext/S0092-8674(14)01497-4?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867414014974%3Fshowall%3Dtrue).[A 3D Map of the Human Genome at Kilobase Resolution Reveals Principles of Chromatin Looping](https://doi.org/10.1016/j.cell.2014.11.021)
- 第一篇insitu HiC的文章，报道了insitu HiC的实验，分析工具(juicer)，单倍型
- 对已有的分析方向/工具/技术/算法的总结，本质上是技术，工具，综述于一体的好文章。

### 基因组
[encode black list](https://www.nature.com/articles/s41598-019-45839-z). [The ENCODE Blacklist: Identification of Problematic Regions of the Genome](https://doi.org/10.1038/s41598-019-45839-z)
- encode计划中有大量的各种类型的数据，发现基因组上有些区域比对情况出现了系统性的偏差，去除了一些高复杂性，组装差的区域。
- [black list下载](https://github.com/Boyle-Lab/Blacklist/)
- encode 提供的一些个人black list： ENCSR636HFF