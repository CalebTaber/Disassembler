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
        addr = split[0]
        src = int(split[1])
        if not src_to_addrs.__contains__(src):
            src_to_addrs[src] = addr

    file.close()
    return src_to_addrs


def read_ass_lines(ass_path, start_addr, end_addr):
    lines = list()
    file = open(ass_path, "r")

    include = False
    for line in file:
        # Empty string signals to read until EOF
        if end_addr == "" and include:
            lines.append(line)
            continue

        if line.startswith(start_addr) or int(line.split()[0][:4], 16) == int(start_addr, 16):
            include = True
        elif line == "" or (end_addr != "" and (int(line.split()[0][:4], 16) == int(end_addr, 16))):
            return lines

        if include:
            lines.append(line)

    return lines


def larger_key(addr_map: dict, key):
    for k in sorted(addr_map.keys()):
        if k > key:
            return k

    return -1


def read_functions(src_name):
    functions = list()
    source = open(src_name, "r")

    src_to_addr = src_addr_dict(src_name)
    fun_name = ""

    line_num = 1
    fun_lines = list()
    for src_line in source:
        if src_to_addr.__contains__(line_num):
            addr = src_to_addr[line_num]
            is_func_decl = func_addr_to_name.__contains__(addr)
            if is_func_decl:
                f = Function(fun_name, fun_lines)
                # print(f.to_string())
                functions.append(f)
                fun_lines = list()
                fun_name = func_addr_to_name[addr]

            next_key = larger_key(src_to_addr, line_num)

            if next_key != -1:
                sl = SourceLine(line_num, src_line, read_ass_lines("./ass/" + src_name + ".ass", addr, src_to_addr[next_key]))
                print(sl.to_string())
                print(sl.ass_text())
                fun_lines.append(sl)
            else:
                sl = SourceLine(line_num, src_line, read_ass_lines("./ass/" + src_name + ".ass", addr, ""))
                print(sl.to_string())
                print(sl.ass_text())
                fun_lines.append(sl)
        else:
            sl = SourceLine(line_num, src_line, list())
            print(sl.to_string())
            print(sl.ass_text())
            fun_lines.append(sl)

        line_num += 1

    return functions


def read_file(src_name):
    return File(src_name, read_functions(src_name))


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
                ass_out.write(ass[4:])
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


def func_addrs_to_names():
    f_names = open("./data/fun_names", "r")

    addr_to_name = dict()

    for line in f_names:
        split = line.split()
        addr_to_name[split[0]] = split[1]

    return addr_to_name


def main():
    # print(str(sys.argv))
    os.system("./script.sh main")

    sequester_assembly()

    global func_addr_to_name
    func_addr_to_name = func_addrs_to_names()

    file_data = list()
    for file_name in open("./data/source_names").readline().split():
        file_data.append(read_file(file_name))

    # Compile HTML file
    newHTMLFile("Example")


if __name__ == "__main__":
    main()
