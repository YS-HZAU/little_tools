import argparse
import pysam
import sys

def BWAALN(insam,outsam,mapq):
    uniqset = {}
    seekmark = insam.tell()
    Nmap = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("XT") == "U" and reads.mapping_quality >= mapq:
            if reads.qname not in uniqset:
                uniqset[reads.qname] = 0
            uniqset[reads.qname] += 1
    insam.seek(seekmark)
    for reads in insam:
        if reads.qname not in uniqset:
            continue
        if uniqset[reads.qname] == 2:
            outsam.write(reads)
            Nmap += 1
    return Nmap/2

def BWAMEM(insam,outsam,mapq):
    uniqset = {}
    seekmark = insam.tell()
    Nmap = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("AS") != reads.get_tag("XS") and reads.mapping_quality >= mapq:
            if reads.qname not in uniqset:
                uniqset[reads.qname] = 0
            uniqset[reads.qname] += 1
    insam.seek(seekmark)
    for reads in insam:
        if reads.qname not in uniqset:
            continue
        if uniqset[reads.qname] == 2:
            outsam.write(reads)
            Nmap += 1
    return Nmap/2

def BOWTIE2(insam,outsam,mapq):
    uniqset = {}
    seekmark = insam.tell()
    Nmap = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.has_tag("AS") and not reads.has_tag("XS") and reads.mapping_quality >= mapq:
            if reads.qname not in uniqset:
                uniqset[reads.qname] = 0
            uniqset[reads.qname] += 1
    insam.seek(seekmark)
    for reads in insam:
        if reads.qname not in uniqset:
            continue
        if uniqset[reads.qname] == 2:
            outsam.write(reads)
            Nmap += 1
    return Nmap/2

def HISAT(insam,outsam,mapq):
    uniqset = {}
    seekmark = insam.tell()
    Nmap = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("NH") == 1 and reads.mapping_quality >= mapq:
            if reads.qname not in uniqset:
                uniqset[reads.qname] = 0
            uniqset[reads.qname] += 1
    insam.seek(seekmark)
    for reads in insam:
        if reads.qname not in uniqset:
            continue
        if uniqset[reads.qname] == 2:
            outsam.write(reads)
            Nmap += 1
    return Nmap/2

def STAR(insam,outsam,mapq):
    uniqset = {}
    seekmark = insam.tell()
    Nmap = 0
    for reads in insam:
        if not reads.is_unmapped and not reads.is_duplicate and not reads.is_secondary and reads.get_tag("NH") == 1 and reads.mapping_quality >= mapq:
            if reads.qname not in uniqset:
                uniqset[reads.qname] = 0
            uniqset[reads.qname] += 1
    insam.seek(seekmark)
    for reads in insam:
        if reads.qname not in uniqset:
            continue
        if uniqset[reads.qname] == 2:
            outsam.write(reads)
            Nmap += 1
    return Nmap/2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True, help="Which software that generated the result [bwa-aln,bwa-mem,bowtie2,hisat,star]")
    parser.add_argument('-i', "--infile", required=True, help="The input file. Automatically recognize sam or bam")
    parser.add_argument('-o', "--outfile", required=True, help="The output file. Automatically recognize sam or bam")
    parser.add_argument('-q', "--mapq", default=0, type=int, help="Remove the low-quality records.[default:0]")
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
    
    if args.type == "bwa-aln":
        Nmap = BWAALN(insam,outsam,args.mapq)
    if args.type == "bwa-mem":
        Nmap = BWAMEM(insam,outsam,args.mapq)
    if args.type == "bowtie2":
        Nmap = BOWTIE2(insam,outsam,args.mapq)
    if args.type == "hisat":
        Nmap = HISAT(insam,outsam,args.mapq)
    if args.type == "star":
        Nmap = STAR(insam,outsam,args.mapq,)
    sys.stderr.write("The saved records is: {0} in {1}\n".format(Nmap,args.infile))
    
    insam.close()
    outsam.close()
