import sys
from math import ceil
import re
import argparse
import subprocess

parser = argparse.ArgumentParser(description="get the interaction from bedpe file")
parser.add_argument("-p","--bedpe",required=True,help="the input bedpe file")
parser.add_argument("-g","--genome",required=True,help="the genome size file")
parser.add_argument("-o","--outputprefix",default="out",type=str,help="the output prefix [out]")
parser.add_argument("-b","--binsize",default=1000000,type=int,help="the resolution [1000000]")
args = parser.parse_args()

def parser_bed(bed):
    flag = None
    n = 0
    with open(bed,'r') as fbed:
        for line in fbed:
            tmp = line.strip().split("\t")
            tmp[3] = int(tmp[3])
            if flag == None:
                if tmp[0] not in mydic:
                    mydic[tmp[0]] = {}
                mydic[tmp[0]][tmp[3]-n] = tmp[3]
            else:
                if flag == tmp[0]:
                    mydic[tmp[0]][tmp[3]-n] = tmp[3]
                else:
                    n = tmp[3]-1
                    if tmp[0] not in mydic:
                        mydic[tmp[0]] = {}
                        mydic[tmp[0]][tmp[3]-n] = tmp[3]
            flag = tmp[0]

def sort_key(s):
    if s:
        try:
            c = re.search("\d+",s)[0] # get the number from string 
        except:
            c = -1
        return int(c)

def parser_bedpe(bedpe,binsize):
    with open(bedpe,'r') as fbedpe:
        for line in fbedpe:
            tmp = line.strip().split("\t")
            b = ceil((int(tmp[1])+int(tmp[2]))/2/binsize) # before
            b = mydic[tmp[0]][b]
            bb = "DNA-"+str(b)
            a = ceil((int(tmp[4])+int(tmp[5]))/2/binsize) # after
            a = mydic[tmp[3]][a]
            aa = "RNA-"+str(a)
            if bb not in interaction:
                interaction[bb] = {}
            if aa not in interaction[bb]:
                interaction[bb][aa] = 0
            interaction[bb][aa] += 1

if __name__ == "__main__":
    ## get the resolution region bed file
#    print("bedtools makewindows -g {0} -w {1} -s {2} | awk -v OFS=\"\\t\" \'{{print $0,NR}}' > {3}.tmp.bed".format(args.genome,args.binsize,args.binsize,args.outputprefix))
    returncode,returnresult = subprocess.getstatusoutput("bedtools makewindows -g {0} -w {1} -s {2} | awk -v OFS=\"\\t\" \'{{print $0,NR}}' > {3}.tmp.bed".format(args.genome,args.binsize,args.binsize,args.outputprefix))
    if returncode != 0:
        print ("[ERROR]: the bedtools maybe have some error : {0}\n".format(returnresult))
        exit()
    ## parser the resolution region bed file
    mydic = {} 
    parser_bed("{0}.tmp.bed".format(args.outputprefix))
    # for k in sorted(mydic.keys()):
    #     for j in sorted(mydic[k].keys()):
    #         print("{0}\t{1}\t{2}".format(k,j,mydic[k][j]))
    # exit()
    ## parser the bedpe file
    interaction = {}
    parser_bedpe(args.bedpe,args.binsize)

    with open("{0}.mat".format(args.outputprefix),'w') as fout:
        for k in sorted(interaction.keys(),key=sort_key):
            for j in sorted(interaction[k].keys(),key=sort_key):
                # print("{0}\t{1}\t{2}".format(k,j,interaction[k][j]))
                fout.write("{0}\t{1}\t{2}\n".format(k,j,interaction[k][j]))