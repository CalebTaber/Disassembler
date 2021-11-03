#! /bin/bash

objdump -d $1 > objdump.out
llvm-dwarfdump --debug-line $1 > dwarf.out

mkdir data
grep -E '[[:alnum:]]{16}\s<.*>' objdump.out > ./data/fun_names
grep -E '\s*name:\s".*.c"' dwarf.out > ./data/file_names
grep -E '0x[[:alnum:]]{16}\s+[0-9]+\s+' dwarf.out > ./data/addrs_src_lines
