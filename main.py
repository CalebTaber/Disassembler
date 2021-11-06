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


class File:
    def __init__(self, name: str, functions: list):
        self.name = name  # Name of file
        self.functions = functions  # List of Function objects


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


def read_ass_up_to(file, stop, incl_last):
    ass = list()

    i = 1
    line = file.readline()
    while line != '':
        prev_line = file.tell()
        if i != 1 and int(line.split()[0], 16) == stop:
            if incl_last:
                ass.append(line)
            else:
                file.seek(prev_line)
            return ass

        ass.append(line)
        i += 1
        line = file.readline()

    return list()


def read_function(fun_name, source_name, src_to_addrs):
    assembly = open("./functions/" + fun_name, "r")
    source = open(source_name, "r")

    source_lines = list()

    line_num = 1
    for src in source:
        # Need to stop reading file when the end of the function is reached
        # We're iterating through the entire source file, but all of the assembly is not
        # contained within

        # Maybe figure out which functions are in which source files and combine the
        # assembly files? (in sequential order)

        if src_to_addrs.__contains__(line_num + 1):
            sl = SourceLine(line_num, src, read_ass_up_to(assembly, src_to_addrs[line_num + 1], False))
            print(sl.to_string())
            print(sl.ass_text())
            source_lines.append(sl)
        elif src_to_addrs.__contains__(line_num - 1):
            # EOF
            sl = SourceLine(line_num, src, read_ass_up_to(assembly, src_to_addrs[line_num], True))
            print(sl.to_string())
            print(sl.ass_text())
            source_lines.append(sl)
        else:
            sl = SourceLine(line_num, src, list())
            print(sl.to_string())
            print(sl.ass_text())
            source_lines.append(sl)
        line_num += 1

    assembly.close()
    source.close()
    return Function(fun_name, source_lines)


def read_functions(source_name, src_to_addrs):
    functions = list()

    fun_names = open("./data/fun_names", "r")
    for addr_name in fun_names:
        split = addr_name.split()
        f_addr = int(split[0], 16)
        f_name = split[1]
        if not list(src_to_addrs.values()).__contains__(f_addr):
            continue
        else:
            functions.append(read_function(f_name, source_name, src_to_addrs))

    return functions


# name of the source file
def read_file(source_name):
    src_to_addrs = src_addr_dict(source_name)
    return File(source_name, read_functions(source_name, src_to_addrs))


def parse_relevant_func_names():
    # Audit fun_names
    # Addr in fun_names must be found in addrs_src_lines
    fun_names = open("./data/fun_names_tmp", "r")
    asl = open("./data/addrs_src_lines", "r")
    source_addrs = list()
    for line in asl:
        split = line.split()
        source_addrs.append(split[0])

    asl.close()

    fun_names_final = open("./data/fun_names", "w")
    for line in fun_names:
        split = line.split()

        # If the function is defined in the given source code
        if source_addrs.__contains__(split[0]):
            fun_names_final.write(line)

    fun_names.close()
    fun_names_final.close()
    os.system("rm ./data/fun_names_tmp")


# def parse_fun_ass():
#     # Parse each relevant function's assembly into its own file
#     fun_file = open("./tmp", "w")  # A file that will contain the assembly of the function
#     write = False  # Whether a line should be written to fun_file or not
#     if not exists("functions"):
#         os.system("mkdir functions")
#     functions = open("./data/fun_names", "r")
#     for function in functions:
#         for line in open("./data/objdump.out", "r"):
#             if line == "\n":
#                 write = False
#                 fun_file.close()
#
#             if write:
#                 fun_file.write(line[4:].replace(":", ""))
#             else:
#                 fsplit = function.split()
#                 if line.startswith(fsplit[0]):
#                     if not fun_file.closed:
#                         fun_file.close()
#                     write = True
#                     fun_file = open("./functions/" + fsplit[1], "w")
#                     fun_file.write(line.replace(":", ""))
#
#     os.system("rm tmp")


def addrs_in_file(file_path):
    file = open(file_path, "r")
    addrs = list()

    for line in file:
        addrs.append(line.split()[0])

    return addrs


def funcs():
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


def main():
    # print(str(sys.argv))
    os.system("./script.sh main")

    #parse_relevant_func_names()
    # parse_fun_ass()
    funcs()

    # file_data = list()
    # source_names = open("./data/source_names")
    # for name in source_names.readline().split():
    #     file_data.append(read_file(name))

    # Compile HTML file
    newHTMLFile("Example")


if __name__ == "__main__":
    main()
