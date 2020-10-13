import sys
import pysam

def main(infile,Nline,outprefix):
    if infile.endswith(".bam"):
        mysam = pysam.AlignmentFile(infile,'rb')
    elif infile.endswith(".sam"):
        mysam = pysam.AlignmentFile(infile,'r')
    else:
        sys.exit("please check the input file, must bam/sam file")
    header = mysam.header

    N = 0
    fl = 1
    flag = True
    mark = None
    for line in mysam:
        if N==0:
            outsam = pysam.AlignmentFile("{0}.tmp.{1}.bam".format(outprefix,fl),'wb',header=header)
            fl += 1
            N = 1
            mark = line.qname
            outsam.write(line)
        else:
            if mark == line.qname:
                flag = True
            else:
                flag = False
            if N < Nline or flag:
                outsam.write(line)
                N += 1
                mark = line.qname
            else:
                outsam.close()
                outsam = pysam.AlignmentFile("{0}.tmp.{1}.bam".format(outprefix,fl),'wb',header=header)
                outsam.write(line)
                N = 1
                fl += 1
                mark = line.qname
    outsam.close()
    mysam.close()

if __name__ == "__main__":
    # input file, N line, outprefix
    main(sys.argv[1],int(sys.argv[2]),sys.argv[3])