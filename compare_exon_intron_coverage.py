import pysam
from scipy import stats

def get_cov(region,samfile):
    A,C,G,T=samfile.count_coverage(region[0],region[1],region[2],read_callback='nofilter')
    return sum(A)+sum(C)+sum(G)+sum(T)

def deal(myexon,samfile):
    myintron = []
    for i,j in enumerate(myexon[:len(myexon)-1]):
        myintron.append(j[0],j[2],myexon[i+1][1])
    exon_cov = []
    intron_cov = []
    for i in myexon:
        exon_cov = get_cov(i,samfile)
    for i in myintron:
        intron_cov = get_cov(i,samfile)
    if len(exon_cov) > 2:
        cc=stats.ttest_ind(exon_cov,intron_cov)
        if cc.pvalue < 0.1:
            return True
        else:
            return False
    else:
        if sum(exon_cov)/sum(intron_cov) > 2 or sum(exon_cov)/sum(intron_cov) < 0.5:
            return True
        else:
            return False

samfile = pysam.AlignmentFile("/public/home/xyhuang/multi-ChIA/meizheng/Drosophila/multichia/rep1/rep1/outs/high.bam", "rb" )
with open("/public/home/xyhuang/Genome/10Xgenome/dm3/dm3.exon.bed",'r') as fin:
'''
chr3L   19744042        19746690        NM_001007095
chr3L   19746777        19746942        NM_001007095
chr3L   19747036        19747265        NM_001007095
chr3L   19747330        19747637        NM_001007095
chr3L   19747706        19747872        NM_001007095
chr3L   19747989        19748322        NM_001007095
chr3L   19748383        19748674        NM_001007095
chr3L   19748794        19748955        NM_001007095
chr3L   19749031        19749203        NM_001007095
'''
    flag = None
    exon = []
    for line in fin:
        tmp = line.strip().split()
        if flag = None and flag != tmp[3]:
            if len(exon) > 1:
                if deal(exon,samfile):
                    print(flag)
            exon = []
        flag = tmp[3]
        exon.append(tmp[0:3])
    if deal(exon,samfile):
        print(flag)
        
samfile.close()