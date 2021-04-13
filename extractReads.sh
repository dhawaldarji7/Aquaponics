

#!/bin/bash
cd ../../
 
source="/home/unhTW/share/mcbs913_2020/aquaponics/conda/project_data/cobb.sr.unh.edu/managed/200314_SN7001360_0492_BHCCMYBCX3_16MerFogartyKapa/reads"
regex="R1"
let i=0
cd "$source"
for dir in "$source"/*;     # list directories in the form "/tmp/dirname/"
do
	
    dir=${dir%*/}   
   echo ${dir##*/}     # remove the trailing "/"
   for file in "$dir"/*; do
    i=$((i + 1))
   if [[ $file =~ $regex ]]; then
	if (( i  == 1 )) ; then
     zcat "$file" | head -10000 > /home/unhTW/share/mcbs913_2020/aquaponics/conda/playdata/idmap/newfile.fq
else 
    zcat "$file" | head -10000 >>/home/unhTW/share/mcbs913_2020/aquaponics/conda/playdata/idmap/newfile.fq
fi
fi
done
   # echo ${dir##*/}    # print everything after the final "/"
done
