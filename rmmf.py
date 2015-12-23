import re

def process_file(symbol_prefix="",
                 command_prefix="",
                 dirname=""):
    with open(dirname + "makefile") as mf:
        for line in mf:
            line = line.rstrip()
            match = re.match("\tcd ([^ \n]*) && make ([^ \n]*)", line)
            if match:
                process_file(symbol_prefix=symbol_prefix + match.group(1) + "_",
                             command_prefix="cd " + dirname + match.group(1) + " && ",
                             dirname=dirname + match.group(1) + "/")
            elif re.match(".PHONY *:", line):
                words = line.split(" ")
                print words[0],
                for x in words[1:]:
                    if x == ":":
                        print x,
                        continue
                    print symbol_prefix + x,
                print
            elif re.search(":", line):
                for x in line.split(" "):
                    if x == ":":
                        print x,
                        continue
                    print symbol_prefix + x,
                print
            elif re.match("\t", line):
                print "\t" + command_prefix + line
            else:
                print line

def main():
    process_file()

main()
