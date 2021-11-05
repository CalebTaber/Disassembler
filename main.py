# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A3
# 11/07/2021

import os
from os.path import exists
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


class SourceLine:
    def __int__(self, number, text, ass):
        self.number = number    # Line number
        self.text = text        # Line text
        self.ass = ass          # Corresponding assembly lines (list of strings)

    def to_string(self):
        return self.number + '\t' + self.text

    def ass_text(self):
        string = ""
        for a in self.ass:
            string += a

        return string


class Function:
    def __init__(self, name, source):
        self.name = name        # Name of the function
        self.source = source    # List of SourceLine objects

    def get_source_lines(self):
        return self.source


class File:
    def __init__(self, name, functions):
        self.name = name            # Name of file
        self.functions = functions  # List of Function objects


def read_ass_lines(end_addr, file):
    ass = list()
    print()


def read_function(name, source_file):
    assembly = open("./functions/" + name, "r")


    return None


# file is the source file
def read_functions(file):
    functions = list()

    fun_names = open("./data/fun_names", "r")
    for addr_name in fun_names.readlines():
        name = addr_name.split()[1]
        functions.append(read_function(name, file))

    return functions


# file is the source file
def read_file(name):
    file = open(name, "r")
    return File(name, read_functions(file))


def parse_relevant_function_names():
    # Audit fun_names
    # Addr in fun_names must be found in addrs_src_lines
    fun_names = open("./data/fun_names_tmp", "r")
    asl = open("./data/addrs_src_lines", "r")
    source_addrs = list()
    for line in asl.readlines():
        split = line.split()
        source_addrs.append(split[0])

    asl.close()

    fun_names_final = open("./data/fun_names", "w")
    for line in fun_names.readlines():
        split = line.split()

        # If the function is defined in the given source code
        if source_addrs.__contains__(split[0]):
            fun_names_final.write(line)

    fun_names.close()
    fun_names_final.close()
    os.system("rm ./data/fun_names_tmp")


def parse_fun_ass():
    # Parse each relevant function's assembly into its own file
    fun_file = open("./tmp", "w")  # A file that will contain the assembly of the function
    write = False  # Whether a line should be written to fun_file or not
    if not exists("functions"):
        os.system("mkdir functions")
    functions = open("./data/fun_names", "r")
    for function in functions.readlines():
        for line in open("./objdump.out", "r"):
            if line == "\n":
                write = False
                fun_file.close()

            if write:
                fun_file.write(line[4:])
            else:
                fsplit = function.split()
                if line.startswith(fsplit[0]):
                    if not fun_file.closed:
                        fun_file.close()
                    write = True
                    fun_file = open("./functions/" + fsplit[1], "w")
                    fun_file.write(line)

    os.system("rm tmp")


def main():
    print(str(sys.argv))
    os.system("./script.sh main")

    parse_relevant_function_names()
    parse_fun_ass()

#    file_names = open("./data/source_names")
#    for name in file_names.readline().split():
#        file_data.append(read_file(name))

    # Compile HTML file
    newHTMLFile("Example")


if __name__ == "__main__":
    main()
