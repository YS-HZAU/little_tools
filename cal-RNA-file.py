import pysam
import sys

if sys.argv[1].endswith(".bam"):
    samfl = pysam.AlignmentFile(sys.argv[1],'rb')
else:
    samfl = pysam.AlignmentFile(sys.argv[1],'r')

total = n = 0
myhash = {}
tongji = {}
flag = []
fq = mtype = typesam = None
# R1&R2_umn(uniq/multi/unmatch)

for line in samfl:
    if line.is_secondary:
        continue
    if line.is_unmapped:
        mtype = 'n'
    elif line.get_tag('NH') == 1:
        mtype = 'u'
    else:
        mtype = 'm'
    if line.is_read2:
        fq = 'R2'
    else:
        fq = "R1"
    
    if n == 0:
        if line.next_reference_id == -1:
            typesam = 'single'
        else:
            typesam = 'pair'
        n += 1

    total += 1
    if mtype not in myhash:
        myhash[mtype] = 0
    myhash[mtype] += 1

    tmpid = fq+"_"+mtype
    if tmpid not in tongji:
        tongji[tmpid] = 0
    tongji[tmpid] += 1

    if typesam == 'pair':
        flag.append(tmpid)
        if len(flag) == 2:
            out = "+".join(flag)
            if out not in tongji:
                tongji[out] = 0
            tongji[out] += 1
            flag = []

for i in ['R1_u','R2_u','R1_n','R2_n','R1_m','R2_m','R1_u+R2_u','R1_m+R2_m','R1_u+R2_n','R1_n+R2_u','R1_m+R2_u','R1_u+R2_m','R1_m+R2_n','R1_n+R2_m','R1_n+R2_n']:
    if i not in tongji:
        tongji[i] = 0
for i in ['n','u','m']:
    if i not in myhash:
        myhash[i] = 0

if typesam == 'single':
    print("this file is single file")
else:
    print("this file is pair file")
print("total reads : {0}".format(total))
print('unmap reads : {0}\t{1:.4f}'.format(myhash['n'],myhash['n']/total))
print('uniqmap reads : {0}\t{1:.4f}'.format(myhash['u'],myhash['u']/total))
print('multimap reads : {0}\t{1:.4f}'.format(myhash['m'],myhash['m']/total))

if typesam == 'pair':
    total = int(total/2)
    print('pair reads count : {0}'.format(total))
    print("read1 unmap read2 unmap reads : {0}\t{1:.4f}".format(tongji['R1_n+R2_n'],tongji['R1_n+R2_n']/total))
    print("read1 unmap read2 uniqmap reads : {0}\t{1:.4f}".format(tongji['R1_n+R2_u'],tongji['R1_n+R2_u']/total))
    print("read1 unmap read2 multimap reads : {0}\t{1:.4f}".format(tongji['R1_n+R2_m'],tongji['R1_n+R2_m']/total))
    print("read1 uniqmap read2 unmap reads : {0}\t{1:.4f}".format(tongji['R1_u+R2_n'],tongji['R1_u+R2_n']/total))
    print("read1 uniqmap read2 uniqmap reads : {0}\t{1:.4f}".format(tongji['R1_u+R2_u'],tongji['R1_u+R2_u']/total))
    print("read1 uniqmap read2 multimap reads : {0}\t{1:.4f}".format(tongji['R1_u+R2_m'],tongji['R1_u+R2_m']/total))
    print("read1 multimap read2 unmap reads : {0}\t{1:.4f}".format(tongji['R1_m+R2_n'],tongji['R1_m+R2_n']/total))
    print("read1 multimap read2 uniqmap reads : {0}\t{1:.4f}".format(tongji['R1_m+R2_u'],tongji['R1_m+R2_u']/total))
    print("read1 multimap read2 multimap reads : {0}\t{1:.4f}".format(tongji['R1_m+R2_m'],tongji['R1_m+R2_m']/total))