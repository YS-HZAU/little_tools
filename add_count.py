import sys

prefix = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])+1

filelist = []
for i in range(start,end):
    fl = open("{0}.{1}.bam.count".format(prefix,i),'r')
    filelist.append(fl)

flag = True
while flag:
    gene = None
    sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = 0
    for index,fl in enumerate(filelist):
        try:
            tmp_line = next(fl)
        except:
            flag = False
            break
        tmp_list = tmp_line.split("\t")
        if gene == None:
            gene = tmp_list[0]
        else:
            if gene != tmp_list[0]:
                sys.exit("it may have some bug")
        sum1 += int(tmp_list[1])
        sum2 += int(tmp_list[2])
        sum3 += int(tmp_list[3])
        sum4 += int(tmp_list[4])
        sum5 += int(tmp_list[5])
        sum6 += int(tmp_list[6])
    if flag:
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(gene,sum1,sum2,sum3,sum4,sum5,sum6))
