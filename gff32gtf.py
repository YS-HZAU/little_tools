import sys

### Operating common files  ###
import gzip
def readFile(infile):
    """
    infile: input file
    return: file handle
    """
    if infile.endswith((".gz","gzip")):
        fin = gzip.open(infile,'rt')
    else:
        fin = open(infile,'r')
    return fin
        
def writeFile(outfile):
    """
    outfile: output file
    return: file handle
    """
    if outfile.endswith((".gz","gzip")):
        fout = gzip.open(outfile,'wt')
    else:
        fout = open(outfile,'w')
    return fout

from collections import OrderedDict
def parseString(mystr):
    """
    mystr: gtf attribution information string
    return: a dictionary
    """
    d = OrderedDict()
    if mystr.endswith(";"):
        mystr = mystr[:-1]
    for i in mystr.strip().split(";"):
        tmp = i.strip().split("=")
        if tmp == "":
            continue
        d[tmp[0]] = tmp[1]
    return d

fin = readFile(sys.argv[1])
fout = writeFile(sys.argv[2])
geneset = set()
transset = set()
exonset = set()
typeset = set()
geneid = set()
gene2name = {}
trans2gene = {}
trans2name = {}
for line in fin:
    tmp = line.strip().split("\t")
    info = parseString(tmp[8])
    if tmp[2] == "gene":
        if  "," in info["ID"]:
            sys.exit("gene error! {0}".format(line))
        if info["ID"] in geneid:
            sys.exit("gene ID not uniq error! {0}".format(line))
        geneid.add(info["ID"])
        fout.write("{0}\t".format("\t".join(tmp[:8])))
        fout.write("gene_id \"{0}\";".format(info["ID"]))
        for k in info.keys():
            if k == "ID":
                pass
            elif k == "Name":
                fout.write(" gene_name \"{0}\";".format(info["Name"]))
                gene2name[info["ID"]] = info["Name"]
            else:
                fout.write(" {0} \"{1}\";".format(k,info[k]))
                geneset.add(k)
        fout.write("\n")
    elif tmp[2] == "mRNA" or tmp[2] == "transcript":
        if  "," in info["ID"]:
            sys.exit("transcript ID error1! {0}".format(line))
        if "," in info["Parent"]:
            sys.exit("transcript Parent error2! {0}".format(line))
        if info["ID"] in trans2gene:
            sys.exit("transcript ID not uniq error3! {0}".format(line))
        trans2gene[info["ID"]] = info["Parent"]
        tmp[2] = "transcript"
        fout.write("{0}\t".format("\t".join(tmp[:8])))
        fout.write("gene_id \"{0}\";".format(trans2gene[info["ID"]]))
        fout.write(" transcript_id \"{0}\";".format(info["ID"]))
        for k in info.keys():
            if k == "ID":
                pass
            elif k == "Parent":
                pass
            elif k == "Name":
                fout.write(" gene_name \"{0}\";".format(gene2name[trans2gene[info["ID"]]])) 
                fout.write(" transcript_name \"{0}\";".format(info["Name"]))
            else:
                fout.write(" {0} \"{1}\";".format(k,info[k]))
                transset.add(k)
        fout.write("\n")
    elif tmp[2] == "exon" or tmp[2] == "CDS":
        if  "," in info["ID"]:
            sys.exit("exon or CDS ID error1! {0}".format(line))
        for ii in info["Parent"].split(","):
            fout.write("{0}\t".format("\t".join(tmp[:8])))
            fout.write("gene_id \"{0}\";".format(trans2gene[ii]))
            fout.write(" transcript_id \"{0}\";".format(ii))
            fout.write(" exon_id \"{0}\";".format(info["ID"]))
            for k in info.keys():
                if k == "ID":
                    pass
                elif k == "Parent":
                    pass
                elif k == "Name":
                    pass
                else:
                    fout.write(" {0} \"{1}\";".format(k,info[k]))
                    exonset.add(k)
            if ii in trans2name:
                fout.write(" gene_name \"{0}\";".format(gene2name[trans2gene[ii]])) 
                fout.write(" transcript_name \"{0}\";".format(trans2name[ii]))
            fout.write("\n")
    else:
        typeset.add(tmp[2])
fin.close()
fout.close()

print("not use gene info:")
for i in geneset:
    print(i)
print("not use transcript info:")
for i in transset:
    print(i)
print("not use exon info:")
for i in exonset:
    print(i)
print("not use type info:")
for i in typeset:
    print(i)