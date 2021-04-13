#!/usr/bin/env python3

import sys
import os
import subprocess

def main():

    forward = sys.argv[1]
    reverse = sys.argv[2]

    base = forward.split("_")[0]
        
    #Fastqc
    print("\nRunning Fastqc...\n")
    outdir = base + "_qc_results"
    subprocess.call('mkdir {}'.format(outdir),shell=True)
    subprocess.call('fastqc {} {} -o {}'.format(forward,reverse,outdir),shell=True)
    
    #Trimmomatic
    print("\nRunning Trimmomatic...\n")
    baseout = base + ".fastq"
    outdir = base + "_trimmomatic_results"
    subprocess.call('trimmomatic PE -phred33 {} {} -baseout {} LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36'.format(forward,reverse,baseout),shell=True)
    
    #SPAdes
    print("\nRunning SPAdes...\n")
    outdir = base + "_spades_results"
    fpaired = base + "_1P.fastq"
    rpaired = base + "_2P.fastq"
    funpaired = base + "_1U.fastq"
    runpaired = base + "_2U.fastq"
    subprocess.call('spades.py -1 {} -2 {} -s {} -s {} -o {}'.format(fpaired,rpaired,funpaired,runpaired,outdir),shell=True)

    #Quast
    print("Running Quast...\n")
    contigs = base + "_spades_results/contigs.fasta"
    outdir = base + "_quast_results"
    subprocess.call('quast.py -1 {} -2 {} -o {} {}'.format(fpaired,rpaired,outdir,contigs),shell=True)

    #Prokka
    print("Running Prokka...")
    outdir = base + "_prokka_results"
    subprocess.call('prokka {} -o {}'.format(contigs,outdir),shell=True)

if __name__ == '__main__':
    main()
