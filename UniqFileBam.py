import argparse
import pysam
import sys

def BWAALN(insam,outsam,mapq,flag,dropsam):
    Nmap = Ndrop = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("XT") == "U" and reads.mapping_quality >= mapq:
            outsam.write(reads)
            Nmap += 1
        else:
            Ndrop += 1
            if flag:
                dropsam.write(reads)
    return Nmap,Ndrop

def BWAMEM(insam,outsam,mapq,flag,dropsam):
    Nmap = Ndrop = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("AS") != reads.get_tag("XS") and reads.mapping_quality >= mapq:
            outsam.write(reads)
            Nmap += 1
        else:
            Ndrop += 1
            if flag:
                dropsam.write(reads)
    return Nmap,Ndrop

def BOWTIE2(insam,outsam,mapq,flag,dropsam):
    Nmap = Ndrop = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.has_tag("AS") and not reads.has_tag("XS") and reads.mapping_quality >= mapq:
            outsam.write(reads)
            Nmap += 1
        else:
            Ndrop += 1
            if flag:
                dropsam.write(reads)
    return Nmap,Ndrop

def HISAT(insam,outsam,mapq,flag,dropsam):
    Nmap = Ndrop = 0
    for reads in insam:
        if not reads.is_unmapped and reads.get_tag("NH") == 1 and reads.mapping_quality >= mapq:
        # if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("NH") == 1 and not reads.has_tag("ZS") and reads.mapping_quality >= mapq:
            outsam.write(reads)
            Nmap += 1
        else:
            Ndrop += 1
            if flag:
                dropsam.write(reads)
    return Nmap,Ndrop

def STAR(insam,outsam,mapq,flag,dropsam):
    Nmap = Ndrop = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("NH") == 1 and reads.mapping_quality >= mapq:
            outsam.write(reads)
            Nmap += 1
        else:
            Ndrop += 1
            if flag:
                dropsam.write(reads)
    return Nmap,Ndrop

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True, help="Which software that generated the result [bwa-aln,bwa-mem,bowtie2,hisat,star]")
    parser.add_argument('-i', "--infile", required=True, help="The input file. Automatically recognize sam or bam")
    parser.add_argument('-o', "--outfile", required=True, help="The output file. Automatically recognize sam or bam")
    parser.add_argument('-q', "--mapq", default=0, type=int, help="Remove the low-quality records.[default:0]")
    parser.add_argument('-f', "--flag", default=False, type=bool, help="Generate the dropped records file.[default:False (False,True)]")
    args = parser.parse_args()
    if args.infile.endswith(".sam"):
        insam = pysam.AlignmentFile(args.infile,'r')
    elif args.infile.endswith(".bam"):
        insam = pysam.AlignmentFile(args.infile,'rb')
    else:
        sys.exit("Unknown input file")
    if args.outfile.endswith(".sam"):
        outsam = pysam.AlignmentFile(args.outfile, 'w', header=insam.header)
    elif args.outfile.endswith(".bam"):
        outsam = pysam.AlignmentFile(args.outfile, 'wb', header=insam.header)
    else:
        sys.exit("Unknown output file")
    dropsam = None
    if args.flag:
        dropsam = pysam.AlignmentFile(args.outfile+".dropped.bam", 'wb', header=insam.header)
    
    if args.type == "bwa-aln":
        Nmap,Ndrop = BWAALN(insam,outsam,args.mapq,args.flag,dropsam)
    if args.type == "bwa-mem":
        Nmap,Ndrop = BWAMEM(insam,outsam,args.mapq,args.flag,dropsam)
    if args.type == "bowtie2":
        Nmap,Ndrop = BOWTIE2(insam,outsam,args.mapq,args.flag,dropsam)
    if args.type == "hisat":
        Nmap,Ndrop = HISAT(insam,outsam,args.mapq,args.flag,dropsam)
    if args.type == "star":
        Nmap,Ndrop = STAR(insam,outsam,args.mapq,args.flag,dropsam)
    sys.stderr.write("The saved records is: {0} in {1}\n".format(Nmap,args.infile))
    sys.stderr.write("The dropped records is: {0} in {1}\n".format(Ndrop,args.infile))
    
    insam.close()
    outsam.close()
    if args.flag:
        dropsam.close()