#!/bin/bash

awk -v var1="$1" -v var2="$2" 'FILENAME==var1{A[$1]=$1} FILENAME==var2{if(A[$1]){print}}' $1 $2 > $3
awk -v var3="$3" '{a[$3]++}!(a[$3]-1)' $3 | awk '{print $3}' | sort -g -k 2 > $4