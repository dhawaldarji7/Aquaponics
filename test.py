#!/usr/bin/python

import sys
import os
import subprocess

def main():

    idfile = raw_input("Enter filename to look for database into: ")
    db = raw_input("Enter database to look for(case-sensitive): ")
    
    db_sorted_file= db +"_idmapping.dat.gz"
    print("Looking for entries of " + db + " in " + idfile)

    #subprocess.call('zgrep {} {} > {}'.format(db,idfile,db_sorted_file), shell=True)
    f=subprocess.Popen(['wc','-l', db_sorted_file], stdout=subprocess.PIPE)

if __name__ == '__main__':
    main()