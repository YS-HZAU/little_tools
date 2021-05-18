import argparse
import sys
import random

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

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Program: downSample\nVersion: 1.0.0\n""")
parser.add_argument('--version', action='version',version='%(prog)s {0} by xyhuang'.format('1.0.0'))
parser.add_argument('-i', "--input", action="store", help="The input file", required=True)
parser.add_argument("-o", "--output", default="output.txt", help="The output prefix [default:output] ")
parser.add_argument('-n', "--number", required = True, help=" If 0<n<=1, take sub-samples proportionally. If n>1, take this number of subsamples")
parser.add_argument('-s', "--seed", help=" The random seed")
args = parser.parse_args()

downsample = 0
if float(args.number) <= 0:
    raise ValueError("please give a value > 0")
fin = readFile(args.input)
lines = []
for line in fin:
    lines.append(line.strip())
fin.close()
nfile = len(lines)
if float(args.number) > nfile:
    downsample = nfile
if float(args.number) <= 1:
    downsample = int(float(args.number) * nfile)
else:
    downsample = int(args.number)
if args.seed != None:
    random.seed(args.seed)

fout = writeFile(args.output)
for i in random.sample(lines,downsample):
    fout.write(i + "\n")
fout.close()