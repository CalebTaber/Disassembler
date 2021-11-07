# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A3
# 11/07/2021

import os
from os.path import exists
import sys
import re


class SourceLine:
    def __init__(self, number: int, text: str, ass: list):
        self.number = number  # Line number
        self.text = text.replace(" ", "&ensp;").replace("\t", "&emsp;").replace("<", "&lsaquo;").replace(">", "&rsaquo;")  # Line text
        self.ass = ass  # Corresponding assembly lines (list of strings)

    def add_links(self):
        for addr in list(func_addr_to_name.keys()):
            name = func_addr_to_name[addr]
            for i in range(0, len(self.ass)):
                ass_line = self.ass[i]
                ass_line = re.sub("<", "&lsaquo;", ass_line)
                ass_line = re.sub(">", "&rsaquo;", ass_line)
                # Give function declarations a name
                ass_line = re.sub("&lsaquo;" + name + "&rsaquo;:$", "<p id=\"" + addr + "\">" + name + "</p>", ass_line)

                # Replace function calls with link to function declaration
                split = ass_line.split()
                if split[-3] == "callq":
                    ass_line = re.sub("&lsaquo;" + name + "&rsaquo;$", "<a href=\"#" + addr + "\">" + name + "</a>", ass_line)

                self.ass[i] = ass_line

    def ass_text(self):
        string = ""
        for i in range(0, len(self.ass)):
            if i == 0:
                string += "&emsp; &emsp;" + self.ass[i].replace(" ", "&ensp;").replace("\t", "&emsp;")
            else:
                string += "<br>&emsp; &emsp;" + self.ass[i].replace(" ", "&ensp;").replace("\t", "&emsp;") + "</br>"

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

        if line.startswith(start_addr) or line.split()[0][:4] == start_addr[-4:]:
            include = True
        else:
            end_substr = end_addr[-4:]
            line_addr = line.split()[0]
            if line == "" or (end_addr != "" and (line_addr[:4] == end_substr or line_addr[-4:] == end_substr)):
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
            end_func = func_addr_to_name.__contains__(addr)
            end_file = line_num == src_file_lengths[src_name]
            if end_func:
                functions.append(Function(fun_name, fun_lines))
                fun_lines = list()
                fun_name = func_addr_to_name[addr]

            if end_file:
                fun_lines.append(SourceLine(line_num, src_line, read_ass_lines("./ass/" + src_name + ".ass", addr, "")))
                functions.append(Function(fun_name, fun_lines))

            next_key = larger_key(src_to_addr, line_num)

            if next_key != -1:
                fun_lines.append(SourceLine(line_num, src_line,
                                            read_ass_lines("./ass/" + src_name + ".ass", addr, src_to_addr[next_key])))
        else:
            fun_lines.append(SourceLine(line_num, src_line, list()))
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

        ass_out = open("./ass/" + src_name + ".ass", "w")
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

    global all_src_addrs
    all_src_addrs = list()
    src_addrs = open("./data/addrs_src_lines", "r")
    for line in src_addrs:
        all_src_addrs.append(line.split()[0])
    src_addrs.close()

    for line in f_names:
        split = line.split()
        if all_src_addrs.__contains__(split[0]):
            addr_to_name[split[0]] = split[1]

    f_names.close()

    return addr_to_name


def create_webpage(file_data, name):
    webpage = open(name + ".html", "w")

    webpage.write(" <!DOCTYPE html>\n"
                  "<html>\n"
                  "<head>\n"
                  "<title>" + name + "</title>\n"
                  "<p>disassem was run at TODO on TODO. Here is the main function: HYPERLINKmainHYPERLINK</p>\n"
                  "</head>\n"
                  "<body>\n")

    for file in file_data:
        webpage.write("<h1>" + file.name + "</h1>\n")
        webpage.write("<table border=1 frame=void rules=rows>\n")
        for function in file.functions:
            for sl in function.source:
                webpage.write("<tr>\n<td valign='top'>\n")
                webpage.write(str(sl.number))
                webpage.write("\n</td>\n<td valign='top'>\n&emsp; ")
                webpage.write(sl.text)
                webpage.write("\n</td>\n<td valign='top'>\n")
                webpage.write(sl.ass_text())
                webpage.write("\n</td>\n</tr>")
        webpage.write("\n</table>\n")

    webpage.write("</body>\n"
                  "</html> ")

    webpage.close()


def main():
    # print(str(sys.argv))
    # os.system("./script.sh main")

    sequester_assembly()

    global func_addr_to_name
    func_addr_to_name = func_addrs_to_names()

    global src_file_lengths
    src_file_lengths = dict()

    file_data = list()
    for file_name in open("./data/source_names").readline().split():
        f = open(file_name)
        src_file_lengths[file_name] = len(f.readlines())
        f.close()
        file_data.append(read_file(file_name))

    create_webpage(file_data, sys.argv[1])


if __name__ == "__main__":
    main()

