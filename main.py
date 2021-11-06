# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A3
# 11/07/2021

import os
from os.path import exists
import sys


def newHTMLFile(name):
    new_file = open(name + ".html", "w")
    new_file.close()
    # Create stack of closing tags that need to be added?
    # Ex: Whenever a <p> is written, add a </p> to the stack


class SourceLine:
    def __init__(self, number: int, text: str, ass: list):
        self.number = number  # Line number
        self.text = text  # Line text
        self.ass = ass  # Corresponding assembly lines (list of strings)

    def to_string(self):
        return str(self.number) + '\t' + self.text

    def ass_text(self):
        string = ""
        for a in self.ass:
            string += a

        return string


class Function:
    def __init__(self, name: str, source: list):
        self.name = name  # Name of the function
        self.source = source  # List of SourceLine objects

    def get_source_lines(self):
        return self.source

    def to_string(self):
        string = self.name
        for sl in self.source:
            string += sl.to_string()

        return string


class File:
    def __init__(self, name: str, functions: list):
        self.name = name  # Name of file
        self.functions = functions  # List of Function objects

    def to_string(self):
        string = self.name
        for func in self.functions:
            string += func.to_string()

        return string


# Maps the source line to the first address of equivalent assembly
def src_addr_dict(source_name):
    file = open("./data/" + source_name + ".out", "r")
    src_to_addrs = dict()
    for line in file:
        split = line.split()
        addr = int(split[0], 16)
        src = int(split[1])
        if not src_to_addrs.__contains__(src):
            src_to_addrs[src] = addr

    file.close()
    return src_to_addrs


def addrs_in_file(file_path):
    file = open(file_path, "r")
    addrs = list()

    for line in file:
        split = line.split()
        # In case the last addr of this file is the first addr of the next
        # We associate the addr with the next file, not this one
        if len(split) == 8 and split[7] == "end_sequence":
            continue
        addrs.append(split[0])

    return addrs


def sequester_assembly():
    src_names = open("./data/source_names", "r")

    for src_name in src_names.readline().split():
        if not exists("ass"):
            os.system("mkdir ass")

        ass_out = open("./ass/" + src_name+ ".ass", "w")
        addrs = addrs_in_file("./data/" + src_name + ".out")

        write = False
        for ass in open("./data/objdump.out", "r"):
            if ass == "\n":
                write = False

            if write:
                ass_out.write(ass)
                continue

            # If a function line
            if ass.endswith(">:\n"):
                addr = ass.split()[0]
                if addrs.__contains__(addr):
                    addrs.remove(addr)
                    write = True
                    ass_out.write(ass)
                else:
                    if write:
                        write = False
                        ass_out.close()
                        break

    src_names.close()


def main():
    # print(str(sys.argv))
    os.system("./script.sh main")

    sequester_assembly()

    # Compile HTML file
    newHTMLFile("Example")


if __name__ == "__main__":
    main()
