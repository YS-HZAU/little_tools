import argparse
import sys
from codefactor import readFile,writeFile

parser = argparse.ArgumentParser(description = " **** ")
parser.add_argument("-i","--input",required=False,help="the input file")
parser.add_argument("-o","--output",required=False,help="the output file")
args = parser.parse_args()

if __name__ == "__main__":
    if args.input == None:
        fin = sys.stdin
    elif args.input == "-":
        fin = sys.stdin
    else:
        fin = readFile(args.input)
    if args.output == None:
        fout = sys.stdout
    else:
        fout = writeFile(args.output)

    for index,line in enumerate(fin):
        if True:
            pass
        else:
            sys.stderr.write("{0} line has error\n".format(index+1))
            sys.stderr.write(line+"\n")
            sys.exit(1)
    
    fin.close()
    fout.close()