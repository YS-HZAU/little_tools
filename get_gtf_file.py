import sys
import re

ios = set()
with open(sys.argv[1],'r') as fin:
    for line in fin:
        tmp = line.split("\t")
        ios.add(tmp[4])

with open(sys.argv[2],'r') as fin:
    for line in fin:
        if re.search(r'transcript_id "(.+?)";',line):
            if re.search(r'transcript_id "(.+?)";',line)[1] in ios:
                print(line,end="")
