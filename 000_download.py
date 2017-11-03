#!/usr/bin/env python2
#encoding: UTF-8


#import sys

import ConfigParser
import csv
import time
import academicdownload as ad


def main():
    

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')    
    subscriptionKey = config.get('main', 'subscriptionKey');

    
    filenames={
        'outQueueFile' : dataDir + "/out-queue-{}.csv",
        'outEntriesFile' : dataDir + "/out-entries-{}.csv",
        'outInvalidFile' :  dataDir + "/out-invalid.csv",
        'inExcludeTopicsFile' :dataDir + "/in-exclude-topics.txt",
        'inIncludeTopicsFile' : dataDir + "/in-include-topics.txt",
        'outQueueSizeFile' : dataDir + "/out-queue-size.txt",
        'seedPapers':dataDir+'/in-seed.csv'
    }

    # copy seed file to queue
    csvInputFile = open(filenames['seedPapers'], 'r')
    csvreader = csv.reader(csvInputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

    csvOutputFile = open(filenames['outQueueFile'].format(0),'w')
    writer = csv.writer(csvOutputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

    for dat in csvreader:
        print dat[0]
        writer.writerow([dat[0]])

    csvOutputFile.close();
    csvInputFile.close();
    
    ###############################################
    # download
    
    for i in xrange(0,3):
        print "Level ", i
        ad.downloadLevel(dataDir, subscriptionKey, i, filenames)
    


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
