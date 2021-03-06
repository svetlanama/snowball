#!/usr/bin/env python2
#encoding: UTF-8
import sys
reload(sys)  
#sys.path.insert(0, '..')
sys.setdefaultencoding('utf8')

import ConfigParser
import csv
import time
import re
from nltk.stem.porter import *
from nltk.corpus import stopwords
import json
import os.path

import topicmodel


# tokenization 

def main():
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')
    
    csvInputFileList = [
        dataDir+'/out-entries-0.csv',
        dataDir+'/out-entries-1.csv',
        dataDir+'/out-entries-2.csv',
        dataDir+'/out-entries-3.csv'
    ]
    
    io = topicmodel.io(dataDir)
    
    # read and tokenize seed entities
    # read and tokenize 1-st level entities
    # save both into csv dictionary
    
    
    regex = re.compile(r"^\d+@", re.IGNORECASE)
    
    # NLP tools:
    tokenizer=topicmodel.CustomTokenizer()
    #tokenizer.stemmer = SnowballStemmer("english")
    tokenizer.stemmer=PorterStemmer()

    tokenizer.validPOSTags = {'NNP':True, 'JJ':True, 'NN':True, 'NNS':True, 'JJS':True, 'JJR':True, 'NNPS':True};
    #tokenizer.validPOSTags = {'NNP':True, 'NN' :True, 'NNS':True, 'NNPS':True,
    #                'JJS':True, 'JJR':True, 'JJ' :True, 
    #                'VB':True , 'VBP':True, 
    #                'RB':True};
    tokenizer.tester = re.compile('^[a-zA-Z]+$')
    tokenizer.stop = set(stopwords.words('english'))
    

    seed_tokens=[]
    all_tokens=[]
    
    cnt=0

    csvSeedOutputFile = open(dataDir+'/tmp-seed-paper-tokens.csv', 'w')
    fieldnames = ['id', 'tokens']
    seed_writer = csv.DictWriter(csvSeedOutputFile, fieldnames=fieldnames, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)
    seed_writer.writeheader()

    csvOutputFile = open(dataDir+'/tmp-all-paper-tokens.csv', 'w')
    fieldnames = ['id', 'tokens']
    writer = csv.DictWriter(csvOutputFile, fieldnames=fieldnames, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)
    writer.writeheader()

    for i in xrange(0, len(csvInputFileList)):
        
        path =csvInputFileList[i]
        print ("path", path)
        if not os.path.isfile(path):
            continue

        csvInputFile = open(path, 'rb')
        csvreader = csv.reader( (x.replace('\0', '') for x in csvInputFile), delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)
        for dat in csvreader:
            # paper Id
            try:
                _tmp=dat[0]
            except IndexError:
                continue
            
            paper_tokens = []

            # keywords
            try:
                kw = [ regex.sub("", s) for s in dat[6].split(";")]
                for tk in kw:
                    paper_tokens.append(tk)
                    if(not tokenizer.wordDictionary.has_key(tk)):
                        tokenizer.wordDictionary[tk] = len(tokenizer.wordDictionary);
            except IndexError:
                print "error extracting keywords"

            # paper text
            w1=""
            try:
                w1=dat[1]
            except IndexError:
                w1=""
                
            w2=""
            try:
                w2=dat[4]
            except IndexError:
                w2=""

            words=unicode(w1+". "+w2, errors='ignore')

            tokens = tokenizer.tokens(words)
            for tk in tokens:
                paper_tokens.append(tk)
                if(not tokenizer.wordDictionary.has_key(tk)):
                    tokenizer.wordDictionary[tk] = len(tokenizer.wordDictionary);

            tk = {'id':dat[0], 'tokens':"+".join(paper_tokens)}

            # print dat[0], words
            cnt = cnt + 1
            if cnt%1000 == 0:
                print i, cnt, tk

            #all_tokens.append(tk)
            writer.writerow(tk)

            if i==0:
                # seed_tokens.append(tk)
                seed_writer.writerow(tk)

        print tokenizer.wordDictionary
        csvInputFile.close();
        
        io.save_dict_as_csv('out-word-dictionary.csv', tokenizer.wordDictionary)

    csvSeedOutputFile.close();
    csvOutputFile.close();

    
    
    
    print len(tokenizer.wordDictionary)," words"

if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0

