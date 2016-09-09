#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# mostly written by Kirill Tsyganov

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def sub_bam_filename(bam_file):
    prefix = bam_file.rsplit('.')
    bam_file = "%s_sub.bam" % prefix[0]
    return bam_file

def sub_sample_bam(bam_file):  
    import subprocess
    # todo handle different subsample
    process = subprocess.Popen(('samtools view -s 0.0003 -b %s > %s') % \
                               (bam_file,
                               sub_bam_filename(bam_file)),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    # todo handle non zero
    process.wait()
    for line in process.stdout:
        print line
    
    for line in process.stderr:
        print line

def sub_index_bam(bam_file):  
    import subprocess

    process = subprocess.Popen(('samtools index %s') % \
                               (bam_file),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    # todo handle non zero
    process.wait()
    for line in process.stdout:
        print line
    
    for line in process.stderr:
        print line        
        
import sys, re, os, argparse
import gzip

def crispr_report_sample_list(vcfFiles):
    sample_list=list()
    
    vcfs = os.listdir(vcfFiles)
    
    for item in sorted(vcfs, key=natural_keys):
        if item.endswith(".vcf.gz") or item.endswith('.vcf'):
            sample_list.append(item)
            
    return sample_list


def crispr_report_sample_info(vcfFiles, bamFiles, vcf, threshold = 1000):
    
    change_list = dict()
    
    # lazy refactor :)
    item = vcf
    
    gziped = item.split('.')[-1]
    gzipped_vcf = False

    if gziped == 'gz':
        vcfFile = gzip.open(os.path.join(vcfFiles, item), 'rb')
        gzipped_vcf = True
    else: 
        vcfFile = open(os.path.join(vcfFiles, item))
        gzipped_vcf = False

    #bamFile = open(os.path.join(bamFiles, item.split("_")[0]+"_sorted.bam"))
    bamFile = item.split(".")[0]
    bamFile = bamFile.split("_")[0]+"_sorted.bam"

    full_bam_path = os.path.join(bamFiles, bamFile)
    sub_sample_bam(full_bam_path)
    sub_index_bam(sub_bam_filename(full_bam_path))

    tmpName = item.split(".")[0]
    name = 'Sample-%s' % tmpName
    counter=0
    check=''
    change_list=list() 

    for i in vcfFile:
        items = i.strip().split()

        if not i.startswith("#"):
            m = re.search("(DP=)([0-9]+)", items[7])
            depth = int(m.group(2))
            chrom = items[0]
            position = int(items[1])
            upstream = position-200
            downstream = position+200
            locus = "%s:%s-%s" % (chrom, upstream, downstream)
            #igvLink = igvTemplate % (bamFile, bamFile, locus)

            # LOGIC HERE
            #print depth
            if m and depth > threshold:

                tmp_changedict = dict()
                tmp_changedict['name'] = name
                tmp_changedict['vcf'] = item
                tmp_changedict['chrom'] = chrom
                tmp_changedict['locus'] = locus
                tmp_changedict['bam'] = bamFile
                tmp_changedict['bam_sub'] = sub_bam_filename(bamFile)
                tmp_changedict['position'] = position
                tmp_changedict['reference'] = items[3]
                tmp_changedict['alternative'] = items[4]
                tmp_changedict['quality'] = items[5]
                tmp_changedict['depth'] = depth    
                print tmp_changedict

                change_list.append(tmp_changedict)
    
    return change_list

#vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
#bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'

#print crispr_report_sample_list(vcfFiles)
#print crispr_report_sample_info(vcfFiles, bamFiles, '22_freebayes.vcf')