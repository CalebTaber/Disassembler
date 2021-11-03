# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A3
# 11/07/2021

import os
import sys

# Use grep for scraping info/pattern matching?

# Command for finding function names and addrs in objdump:      grep -E '[[:alnum:]]{16}\s<.*>' objdump.out
# Command for finding file names in dwarf:                      grep -E '\s*name:\s".*.c"' dwarf.out
# Command for assembly addrs and source lines from dwarf:       grep -E '0x[[:alnum:]]{16}\s+[0-9]+\s+' dwarf.out
#   Can tell where functions end b/c of "is_stmt end_sequence"
# Command for getting source line:                              sed 'n!d' file, where n = line num, and file is the file


def newHTMLFile(name):
    newFile = open(name + ".html", "w")
    newFile.write("<!DOCTYPE html>\n"
                  "<html>\n"
                  "<head>\n"
                  "<title>Disassembler</title>\n"
                  "</head>\n"
                  "<body>\n"
                  "<h1>Fuckin shit</h1>\n"
                  "<p>Is what this project is gonna be</p>\n"
                  "</body>\n"
                  "</html>")
    # Create stack of closing tags that need to be added?
    # Ex: Whenever a <p> is written, add a </p> to the stack


class FileInfo:
    def __init__(self, name):
        self.name = name
        self.lines = None
        self.functions = None


print(str(sys.argv))

objdump = "objdump -d " + sys.argv[1] + " > objdump.out"
dwarfdump = "llvm-dwarfdump --debug-line " + sys.argv[1] + " > dwarf.out"
objExit = os.system(objdump)
dwarfExit = os.system(dwarfdump)

print("Result: ", objExit)
print("Result: ", dwarfExit)

newHTMLFile("Example")

