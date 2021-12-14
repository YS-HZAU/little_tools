# 参考文献
### 无连接三维基因组测序
[SPRITE](https://www.cell.com/cell/fulltext/S0092-8674(18)30636-6?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867418306366%3Fshowall%3Dtrue).[Higher-Order Inter-chromosomal Hubs Shape 3D Genome Organization in the Nucleus](https://doi.org/10.1016/j.cell.2018.05.024).<br/>
- 在反应池中给蛋白-DNA复合物上的DNA序列上连接上特别设计的barcode序列。用这个barcode序列来标记一个个的DNA复合物。默认是同一个标记的DNA是在空间上靠近的。
- 分析中AB compartment用的[cworld](https://github.com/dekkerlab/cworld-dekker)，TAD用的[matrix2insulation.pl](https://github.com/dekkerlab/crane-nature-2015/tree/master/scripts)，Loop用的和juicer一样的方法（自己开发）。可能还是存在数据量不够的问题，尝试用juicer做AB compartment，TAD，Loop不能得到好结果

