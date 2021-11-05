#!/bin/bash
# Caleb Taber (ctaber2@u.rochester.edu)
# CSC 254, A4
# 11/07/2021 


objdump -d $1 > objdump.out
llvm-dwarfdump --debug-line $1 > dwarf.out


if [ ! -d "./data" ]; then
  mkdir data
fi

# Extract function names and addrs from objdump output
grep -E '[[:alnum:]]{16}\s<.*>' objdump.out | sed 's/<//g' | sed 's/>//g' | sed 's/://g' | perl -0 -pe 's/\n\Z//' > ./data/fun_names

# Add source file names to an array
source_names=()
i=0
# Command here extracts the source file names from the dwarfdump output
for name in $(grep -oE '".*.c"' dwarf.out | perl -0 -pe 's/\n\Z//' | sed 's/"//g' | uniq)
do
  source_names[i]=$name
  i=$((i+1))
done

grep -E '0x[[:alnum:]]{16}\s+[0-9]+\s+' dwarf.out | perl -0 -pe 's/\n\Z//' > ./data/addrs_src_lines


# Want to separate assembly lines from addrs_src_lines into separate files according to the file name order in source_names

# Gets line numbers of 'is_stmt end_sequence'
grep -En 'is_stmt end_sequence' ./data/addrs_src_lines | grep -oE '^[[:digit:]]+' | perl -0 -pe 's/\n\Z//' > ./data/line_nums


# Put assembly lines into individual files according to source code file
name_index=0
s=1
ass_len=$(wc -l < ./data/addrs_src_lines)
for e in $(grep -E '.' ./data/line_nums)
do
  output_name=./data/${source_names[$name_index]}.out
  if [ -f $output_name ]; then
    rm $output_name
  fi
  
  sed -n "$s,${e}p" ./data/addrs_src_lines | perl -0 -pe 's/\n\Z//' >> $output_name
  name_index=$((name_index+1))
  s=$((e+1))
done

