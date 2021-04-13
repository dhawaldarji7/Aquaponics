#!/usr/bin/env python3

import subprocess
import os
import gzip

vfdb_file = "VFDB_core_pro.fas"
outfile = "ypnpfile.txt"

print("Getting the YP and NP id's from " + vfdb_file)
subprocess.call('zgrep "YP_\|NP_\" {} | cut -d"|" -f2 | cut -d")" -f1 > {}'.format(vfdb_file,outfile),shell=True)

myNames = set()
f = open(outfile,'r')

for line in f:
    if ".1" in line:
        myNames.add(line.strip("\n"))
    else:
        myNames.add(line.strip("\n")+".1")

file1  = gzip.open('release70.bacterial-reannotation-report.txt.gz','r')

print("\nCreating dictionary")
wpdict={}
for line in file1:
    lsplit=line.decode("utf-8").split("\t")
    wpdict[lsplit[8]]=lsplit[16]

print("\nSearching the dictionary\n")
count = 0
wpf = open('wpfile.txt','w')
for element in myNames:
    if wpdict.get(element)!=None:
        count+=1
        wpf.write(wpdict.get(element)+'\n')
        
print("Found: {} WP id's matching to corresponding YP/NP id's out of {}".format(count,len(myNames)))
wpf.close()

#Getting all the WP entries from idmapping file
idmapping = "idmapping.dat.gz"
wpidm = "wpidm.txt"
subprocess.call('zgrep "WP_" {} > {}'.format(idmapping,wpidm),shell=True)

wpidmf = open("wpidm.txt",'r')
wpf = open('wpfile.txt','r')
wpuprotf = open("wpuprot.txt",'w')

wp_set = set()
for line in wpf:
    wp_set.add(line)
    
for line in wpidmf:
    if line.split("\t")[2] in wp_set:
        wpuprotf.write(line.split("\t")[0]+'\n')
wpuprotf.close()

wpuprotf = open("wpuprot.txt",'r')
wpuprot_set = set()
for line in wpuprotf:
    wpuprot_set.add(line.strip("\n"))

wpuniref = open("wpuniref.txt",'w')
idm = open("UniRef90_idmapping.dat.gz",'r')
for line in idm:
    if "UniRef90" in line.split("\t")[1]:
        if line.split("\t")[0] in wpuprot_set:
            wpuniref.write(line.split("\t")[2]+'\n')
wpuniref.close()

wpuniref = open("wpuniref.txt",'r')
wpuniref_set = set()
for line in wpuniref:
    wpuniref_set.add('>'+line.strip("\n"))

uniref = gzip.open("uniref90.fasta.gz",'r')
wp_uni_data = open("wp_uni_data.txt",'w')
write=False
for line in uniref:
    if b'>' in line:
        key = line.decode("utf-8").split(" ")[0]
        if key in wpuniref_set:
            write=True
        else:
            write=False
    if write:
        wp_uni_data.write(line.decode("utf-8"))

print("Completed.")


    


