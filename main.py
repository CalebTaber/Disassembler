# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A3
# 11/07/2021

import os
import sys

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


class Line:
    def __int__(self, number, text):
        self.number = number
        self.text = text


class Function:
    def __init__(self, name, assembly, source):
        self.name = name
        self.assembly = assembly
        self.source = source


class File:
    def __init__(self, name, functions):
        self.name = name  # String
        self.functions = functions  # List of Function objects


print(str(sys.argv))

# objdump = "objdump -d " + sys.argv[1] + " > objdump.out"
# dwarfdump = "llvm-dwarfdump --debug-line " + sys.argv[1] + " > dwarf.out"
# objExit = os.system(objdump)
# dwarfExit = os.system(dwarfdump)

newHTMLFile("Example")
