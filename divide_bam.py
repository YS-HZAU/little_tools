import argparse
import pysam
import re
import sys

parser = argparse.ArgumentParser(description = "divider bam into uniq/multi/unmap/lowuniq")
parser.add_argument("-i","--input",required=True,help="the input bam/sam file")
parser.add_argument("-t","--type",required=True,help="the map software [bwaaln bwamem bowtie2 hisat2]")
parser.add_argument("-q","--qual",default=20,type=int,help="the lowuniq quality limit [default:20]")
parser.add_argument("-f","--format",default="bam",help="the output format:bam or sam [default:bam]")
parser.add_argument("-p","--outtype",default="all",help="you can choose just one or more(comma separated),default will output all[all,uniq,lowuniq,multi,unmap]")
parser.add_argument("-o",'--outputprefix',default="out",help="the output prefix [default:out]")
args = parser.parse_args()

def readfile(fin):
    if fin.endswith("bam"):
        mysam = pysam.AlignmentFile(fin,'rb')
    else:
        mysam = pysam.AlignmentFile(fin,'r')
    return mysam

def bwaaln_check(reads,outhandle,outcount,qual):
    if reads.is_unmapped:
        if 'unmap' in outhandle:
            outhandle['unmap'].write(reads)
            outcount['unmap'] += 1
    elif reads.get_tag('XT')=="U":
        if reads.mapping_quality < qual:
            if 'lowuniq' in outhandle:
                outhandle['lowuniq'].write(reads)
                outcount['lowuniq'] += 1
        else:
            if 'uniq' in outhandle:
                outhandle['uniq'].write(reads)
                outcount['uniq'] += 1
    elif reads.get_tag('XT')=="R":
        if 'multi' in outhandle:
            outhandle['multi'].write(reads)
            outcount['multi'] += 1
    elif reads.get_tag('XT')=="N":
        if 'unmap' in outhandle:
            outhandle['unmap'].write(reads)
            outcount['unmap'] += 1
    else:
        print("it has some error")
        print(reads)
        exit()

def bwamem_check(reads,outhandle,outcount,qual):
    if reads.is_unmapped:
        if 'unmap' in outhandle:
            outhandle['unmap'].write(reads)
            outcount['unmap'] += 1
    elif reads.get_tag('AS') != reads.get_tag('XS'):
        if reads.mapping_quality < qual:
            if 'lowuniq' in outhandle:
                outhandle['lowuniq'].write(reads)
                outcount['lowuniq'] += 1
        else:
            if 'uniq' in outhandle:
                outhandle['uniq'].write(reads)
                outcount['uniq'] += 1
    elif reads.get_tag('AS') == reads.get_tag('XS'):
        if 'multi' in outhandle:
            outhandle['multi'].write(reads)
            outcount['multi'] += 1
    else:
        print("it has some error")
        print(reads)
        exit()

def bowtie2_check(reads,outhandle,outcount,qual):
    if reads.is_unmapped:
        if 'unmap' in outhandle:
            outhandle['unmap'].write(reads)
            outcount['unmap'] += 1
    elif not reads.has_tag('XS'):
        if reads.mapping_quality < qual:
            if 'lowuniq' in outhandle:
                outhandle['lowuniq'].write(reads)
                outcount['lowuniq'] += 1
        else:
            if 'uniq' in outhandle:
                outhandle['uniq'].write(reads)
                outcount['uniq'] += 1
    elif reads.get_tag('AS') != reads.get_tag('XS'):
        if reads.mapping_quality < qual:
            if 'lowuniq' in outhandle:
                outhandle['lowuniq'].write(reads)
                outcount['lowuniq'] += 1
        else:
            if 'uniq' in outhandle:
                outhandle['uniq'].write(reads)
                outcount['uniq'] += 1
    elif reads.get_tag('AS') == reads.get_tag('XS'):
        if 'multi' in outhandle:
            outhandle['multi'].write(reads)
            outcount['multi'] += 1
    else:
        print("it has some error")
        print(reads)
        exit()

def hisat2_check(reads,outhandle,outcount,qual):
    if reads.is_unmapped:
        if 'unmap' in outhandle:
            outhandle['unmap'].write(reads)
            outcount['unmap'] += 1
    elif reads.get_tag('NH') == 1:
        if reads.mapping_quality < qual:
            if 'lowuniq' in outhandle:
                outhandle['lowuniq'].write(reads)
                outcount['lowuniq'] += 1
        else:
            if 'uniq' in outhandle:
                outhandle['uniq'].write(reads)
                outcount['uniq'] += 1
    elif int(reads.get_tag('NH')) > 1:
        if 'multi' in outhandle:
            outhandle['multi'].write(reads)
            outcount['multi'] += 1
    else:
        print("it has some error")
        print(reads)
        exit()


if __name__ == "__main__":
    # output type
    outtype = set()
    for i in args.outtype.split(','):
        if not re.search(r"all|uniq|lowuniq|multi|unmap",i):
            sys.stderr("maybe check outtype,it must be all,uniq,lowuniq,multi,unmap")
            exit()
        else:
            match = re.search(r"all|uniq|lowuniq|multi|unmap",i)[0]
            if match == "all":
                outtype = set(['uniq','lowuniq','multi','unmap'])
            else:
                outtype.add(match)
    print("out type:{0}".format(",".join(outtype)))
    print("input file:{0}".format(args.input))
    samfile = readfile(args.input)

    # output format
    outhandle = {}
    outcount = {}
    if args.format == "bam":
        for i in outtype:
            tmppath = "{0}.{1}.{2}".format(args.outputprefix,i,args.format)
            outhandle[i] = pysam.AlignmentFile(tmppath,'wb',header=samfile.header)
            outcount[i] = 0
    else:
        for i in outtype:
            tmppath = "{0}.{1}.{2}".format(args.outputprefix,i,args.format)
            outhandle[i] = pysam.AlignmentFile(tmppath,'w',header=samfile.header)
            outcount[i] = 0
    
    nn = 0
    for reads in samfile:
        nn += 1
        if nn%1000000==0:
            print("deal with {0} M reads".format(int(nn/1000000)))
        if args.type == "bwaaln":
            bwaaln_check(reads,outhandle,outcount,args.qual)
        if args.type == "bwamem":
            bwamem_check(reads,outhandle,outcount,args.qual)
        if args.type == "bowtie2":
            bowtie2_check(reads,outhandle,outcount,args.qual)
        if args.type == "hisat2":
            hisat2_check(reads,outhandle,outcount,args.qual)

    for i,j in outcount.items():
        print("{0}:{1}".format(i,j))
        outhandle[i].close()
    samfile.close()