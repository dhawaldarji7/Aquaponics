#!/usr/bin/env python3

import sys
import os
import subprocess
import gzip

def main():

    idfile = sys.argv[1]    #The original file with all entries.
    db = input("Enter database to look for(case-sensitive): ")      #Database(DB) we are looking for
    
    db_sorted_file= db + "_" + idfile     #Output file with the required database entries 
    uniref90_file = "UniRef90_" + idfile        #Output file with all the uniref90 entries
    final_file = db + "_UniRef90_" + idfile         #Output file with UniRef entries for every DB entry we looked for
    unique_file = "Unique_" + final_file                #Output file with only the unique UniRef entries for DB
   
    #Looking for our database in the original file
    print("\nLooking for entries of " + db + " in " + idfile)
    #subprocess.call('zgrep {} {} > {}'.format(db,idfile,db_sorted_file), shell=True)
    print("\nCompleted search for " + db + " in " + idfile + ".Results in " + db_sorted_file)

    #Filtering out all the uniref90 entries in original file
    print("\nExtracting the UniRef90 entries in " + idfile)
    #subprocess.call('zgrep "UniRef90" {} > {}'.format(idfile,uniref90_file), shell=True)
    print("\nCompleted extracting the UniRef90 entries from " + idfile + ".Results in " + uniref90_file)

    #Looking for PATRIC entries with a UniRef90 entry
    print("\nLooking for " + db + " entries with UniRef90 entry in " + uniref90_file)
    #subprocess.call('./db_uniref.sh {} {} {} {}'.format(db_sorted_file,uniref90_file,final_file,unique_file),shell=True)
    print("\nSuccessfully mapped " + db + " entries with UniRef90 entry in " + uniref90_file + ".Results in " + final_file)
    print("\nUnique entries of UniRef90 can be found in " + unique_file)

    #Creating set of all the cross-reference id's
    unique_uniref_set = set()
    with open(unique_file,'r') as f:
        for line in f:
            unique_uniref_set.add(">" + line.strip("\n"))

   #looking up for the cross-reference id's in uniref90.fasta.gz
    uf = open("upat.fasta.gz",'w')
    with gzip.open("uniref90.fasta.gz",'r') as u:
        for index,line in enumerate(u):
            if b'>' in line:
                linedec = line.decode("utf-8")
                key = linedec.split(" ")[0]
                if key in unique_uniref_set:
                    i=index+1
                    uf.write(line.decode("utf-8"))  #we write it to a new file
                    for i,nextline in enumerate(u):                        #this loop writes all the dat about the key in the new file
                        if b'>' not in nextline:
                            uf.write(nextline.decode("utf-8"))
                        else:
                            break
                            
if __name__ == '__main__':
    main()