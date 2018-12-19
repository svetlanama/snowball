#!/usr/bin/env python2
#encoding: UTF-8
import sys
reload(sys)
sys.path.insert(0, '..')
sys.setdefaultencoding('utf8')

import ConfigParser
# import academicdownload as ad
import csv
import re
import nltk
from nltk.stem.porter import *
import numpy
import random
import time
import topicmodel
from nltk.corpus import stopwords
import academicdownload as ad
import Queue
import json
 

# map documents to topic using the topic model

# The Jensen–Shannon divergence (JSD) M + 1 ( A ) × M + 1 ( A ) → [ 0 , ∞ ) {\displaystyle M_{+}^{1}(A)\times M_{+}^{1}(A)\rightarrow [0,\infty {})} M_{+}^{1}(A)\times M_{+}^{1}(A)\rightarrow [0,\infty {}) is a symmetrized and smoothed version of the Kullback–Leibler divergence D ( P ∥ Q ) {\displaystyle D(P\parallel Q)} D(P\parallel Q). It is defined by
# J S D ( P ∥ Q ) = 1 2 D ( P ∥ M ) + 1 2 D ( Q ∥ M ) {\displaystyle {\rm {JSD}}(P\parallel Q)={\frac {1}{2}}D(P\parallel M)+{\frac {1}{2}}D(Q\parallel M)} {{\rm {JSD}}}(P\parallel Q)={\frac {1}{2}}D(P\parallel M)+{\frac {1}{2}}D(Q\parallel M)
# where M = 1 2 ( P + Q ) {\displaystyle M={\frac {1}{2}}(P+Q)} M={\frac {1}{2}}(P+Q) 
def js_divergence(v1, v2):
    # symmetric KL - divergence
    v0=[ 0.5*(v1[i]+v2[i]) for  i in xrange(0, len(v1))]
    s = 0
    for i in xrange(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log( ( v1[i] + 0.000001) / ( v0[i] + 0.000001 ) )
        # abs(v1[i]-v2[i])
    for i in xrange(0, len(v1)):
        s = s + (v2[i] + 0.000000000001) * numpy.log( ( v2[i] + 0.000001) / ( v0[i] + 0.000001 ) )
    return s*0.5

# simple KL - divergence
def kl_divergence(v1, v2):
    
    s = 0
    for i in xrange(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log( ( v1[i] + 0.000001) / ( v2[i] + 0.000001 ) )
    return s

# symmetric KL - divergence
def skl_divergence(v1, v2):
    
    s = 0
    for i in xrange(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log( ( v1[i] + 0.000001) / ( v2[i] + 0.000001 ) )
        # abs(v1[i]-v2[i])
    for i in xrange(0, len(v1)):
        s = s + (v2[i] + 0.000000000001) * numpy.log( ( v2[i] + 0.000001) / ( v1[i] + 0.000001 ) )
    return s*0.5


# S2JSD measure
# https://pdfs.semanticscholar.org/77b1/9a491e14697bd87e56b0bd7fa1d6c8e9f857.pdf
def s2jsd_divergence(v1, v2):
    
    s = 0
    for i in xrange(0, len(v1)):
        s = s + (v1[i] + 0.000001) * numpy.log( 2* ( v1[i] + 0.000001 ) / ( v1[i] + v2[i] + 0.000002 ) )
        
    for i in xrange(0, len(v1)):
        s = s + (v2[i] + 0.000001) * numpy.log( 2* ( v2[i] + 0.000001 ) / ( v1[i] + v2[i] + 0.000002 ) )
    return numpy.sqrt(s)


# https://en.wikipedia.org/wiki/Hellinger_distance
def hellinger_distance(v1, v2):
    s = 0
    for i in xrange(0, len(v1)):
        d=numpy.sqrt(v1[i])-numpy.sqrt(v2[i])
        s = s + d*d
    return numpy.sqrt(0.5 * s)


# difference=kl_divergence # run 1
difference=skl_divergence # run 2
# difference=js_divergence # run 3

'''


'''
def compare(x, y):
    if x['p'] > y['p']:
        return -1
    elif x['p'] < y['p']:
        return 1
    else:
        return 0
'''


'''
def flatten(entry):

    return {
            'entryId': entry['entryId'],
            'url':entry['url'],
            'text': re.sub(r"\r|\n|\t", " ", entry['text']),
            'keywords':entry['keywords'],
            'referencesTo':";".join([str(s) for s in entry['referencesTo'] ]   ),
            'tokens':";".join(entry['tokens']),
            'referencedBy':";".join(entry['referencedBy']),
            'topics':";".join([ str(t) for t in entry['topics'] ]),
            'ECC':str(entry['ECC']),
            'dist':str(entry['distanceToSeed']),
            'year':str(entry['year'])
    }











'''



'''
class LocalTokenizer:
    def __init__(self):
        self.validPOSTags = {}
        self.stemmer = False # PorterStemmer()
        self.tester = False  # re.compile('^[a-zA-Z]+$')
        self.wordDictionary = {}
        self.stop = set([])

    def tokens(self, string):
        try:
            text = nltk.word_tokenize(string)
        except UnicodeDecodeError:
            text = nltk.word_tokenize(unicode(string, errors='ignore'))
            
        taggedWords = nltk.pos_tag(text)
        tokens = []
        stopwords=[]
        unknownwords=[]
        for tw in taggedWords:
            #print tw
            if(self.validPOSTags.has_key(tw[1])):
                theWord = tw[0].lower()
                # print theWord, tester.match(theWord)

                try:
                    if(self.tester.match(theWord)):
                        theWord = self.stemmer.stem(tw[0].lower()).encode('utf-8')
                    if self.wordDictionary.has_key(theWord) :
                        tokens.append(theWord)
                    elif theWord in self.stop:
                        stopwords.append(theWord)
                    else:
                        unknownwords.append(theWord)
                except IndexError:
                    continue

        return (tokens, stopwords, unknownwords)
'''



'''
def main():
    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    restEndpoint=json.loads(config.get('main', 'restEndpoint'))
    
    dataDir = config.get('main', 'dataDir')
    maxDistance = config.getfloat('main', 'maxDistance')
    subscriptionKey = config.get('main', 'subscriptionKey');
    subsampleFraction = config.getfloat('main', 'subsampleFraction')


    logFile=dataDir + "/out-snowball.log"

    api = ad.Api(subscriptionKey, restEndpoint)

    maExcludeTopicsFile = dataDir + "/in-exclude-topics.txt"
    msAcademicExcludeTopicsIds = set(api.loadList(maExcludeTopicsFile));

    maIncludeTopicsFile = dataDir + "/in-include-topics.txt"
    msAcademicIncludeTopicsIds = api.loadList(maIncludeTopicsFile)

    #maQueueSizeFile = dataDir + "/out-queue-size.txt"
    #maInvalidFile = dataDir + "/out-invalid.csv"

    #regex = re.compile(r"^\d+@", re.IGNORECASE)

    io = topicmodel.io(dataDir)
    
    # read wordDictionary
    wordDictionary = io.load_csv_as_dict('out-word-dictionary-reduced.csv')

    wwcovarReduced = numpy.load(dataDir + '/tmp-joint-probability-reduced.npy')
    
    topicModel = numpy.load(dataDir + '/out-TopicModel.npy')
    topicModel = topicModel.item()

    model = topicmodel.model(dataDir)
    model.set_word_dictionary(wordDictionary)
    model.load_topic_model(wwcovarReduced, topicModel)

    # NLP tools:
    tokenizer=LocalTokenizer()
    
    #tokenizer.stemmer = SnowballStemmer("english")
    tokenizer.stemmer=PorterStemmer()

    tokenizer.wordDictionary = wordDictionary
    
    tokenizer.validPOSTags = {'NNP':True, 'JJ':True, 'NN':True, 'NNS':True, 'JJS':True, 'JJR':True, 'NNPS':True};
    tokenizer.tester = re.compile('^[a-zA-Z]+$')
    tokenizer.stop = set(stopwords.words('english'))


    

    
    acceptedDocs = set()
    indexedDocs = set()
    seedIds = []
    fullDictionary = {}

    apiCallCounter=0

    # file to write citaton network
    csvOutputFile = open(dataDir + '/out-citation-network.csv', 'w')
    fieldnames = ['entryId','dist','url','ECC','year','text','keywords','referencesTo','tokens','referencedBy','topics']
    writer = csv.DictWriter(csvOutputFile, fieldnames=fieldnames, delimiter="\t", quotechar='',escapechar="\\", quoting=csv.QUOTE_NONE)
    writer.writeheader()
    
    currentLevelQueue = Queue.Queue()
    # fill in the seed queue
    # read seed docs from CSV file
    # ms-academic-entries-0.csv
    # load all the entries into fullDictionary and into seedIds
    #     entryId : [entryId: , url: , text:"..." , tokens:[], referencesTo:[...]  referencedBy:[...] , topics:[]]
    csvInputFile = open(dataDir + '/in-seed.csv', 'r')
    csvreader = csv.reader(csvInputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

    random.seed()
    for dat in csvreader:
        if random.random() < subsampleFraction :
            docId = dat[0]
            #print docId
            #seedIds.append(str(docId))
            currentLevelQueue.put(str(docId))
        
    csvInputFile.close();
    # print "currentLevelQueue.qsize=",currentLevelQueue.qsize()
    # return

    # fill-in the zero level with seed enties
    entryIds=[]

    nextLevelQueue = Queue.Queue()

    while not currentLevelQueue.empty():
        docId = currentLevelQueue.get()
        print docId
        entryIds.append(docId)
        if len(entryIds)>=80 or currentLevelQueue.empty():

            # download linked publications
            linkedPublications = []

            # load items from queue
            publications = api.loadByIds(entryIds, msAcademicIncludeTopicsIds, False)
            # return
            apiCallCounter = apiCallCounter + 1
            print "apiCallCounter=", apiCallCounter

            #print ""
            #print "referencesTo:"
            for p in publications:
                indexedDocs.add(p.entryId)
                #print p.entryId, p.entryTitle

                # tokenize publications
                # get topic probabilities
                # ----- tokenize - begin -----------------------------------
                tokens = []

                # keywords
                kw = [ s.topicName for s in p.topics]
                for tk in kw:
                    tokens.append(tk)

                # paper text
                # words=unicode(p.entryTitle + ". "+ p.entryAbstract, errors='ignore')
                words=p.entryTitle.encode("utf-8") + ". "+ p.entryAbstract.encode("utf-8")
                _tokens, _stopwords, _unknownwords = tokenizer.tokens(words)
                for tk in _tokens:
                    tokens.append(tk)
                # ----- tokenize - end -------------------------------------

                # apply topic model
                topics = model.topics_from_doc(tokens)

                fullDictionary[str(p.entryId)] = {
                    'entryId': p.entryId,
                    'url':p.entryURL,
                    'text': words,
                    'keywords':";".join([ s.toCSV() for s in p.topics]),
                    'tokens':tokens,
                    'referencesTo':p.referencesTo,
                    'referencedBy':[],
                    'ECC':p.ECC,
                    'year':p.entryPublished,
                    'topics':topics.tolist(),
                    'distanceToSeed':0
                }
                seedIds.append(str(p.entryId))


                print "adding-seed: id",p.entryId, " dist=",0," ECC=",p.ECC," year=", p.entryPublished," title=",p.entryTitle

                # update next level queue
                nextLevelQueue.put(p.entryId)
                for docId in p.referencesTo:
                    nextLevelQueue.put(docId)

                indexedDocs.add(p.entryId)
                acceptedDocs.add(p.entryId)
                writer.writerow(flatten(fullDictionary[str(p.entryId)]))

            entryIds=[]


    currentLevelQueue = nextLevelQueue
    # print(list(currentLevelQueue))

    logMessages=[]

    # iterate over snowball levels
    for level in xrange(0,10):
        print "============== level ", level
        #maQueueFile = dataDir + "/ms-academic-queue-" + str(level) + ".csv"
        
        nextLevelQueue = Queue.Queue()
        
        inputIds=[]
        inputRIds=[]
        linkedPublications=[]
        while not currentLevelQueue.empty():
            docId = currentLevelQueue.get()
            #print docId

            if docId in indexedDocs:
               inputRIds.append(docId)
            else:
               inputIds.append(docId)
               
            if len(inputRIds)>=80 or currentLevelQueue.empty():
                
                print 'get publications referencing the indexed ones'
                
                linkedPublications = api.loadByRIdsExtended(inputRIds, msAcademicIncludeTopicsIds, False)
                inputRIds = []
                
                apiCallCounter = apiCallCounter + 1
                print "apiCallCounter=", apiCallCounter

            if len(inputIds)>=80 or currentLevelQueue.empty():
                
                print 'get publications referenced with indexed ones'
                
                linkedPublications = api.loadByIds(inputIds, msAcademicIncludeTopicsIds, False)
                inputIds = []

                apiCallCounter = apiCallCounter + 1
                print "apiCallCounter=", apiCallCounter

            if len(linkedPublications)>0:
                #distances=[]
                for p in linkedPublications:
                    
                    if not fullDictionary.has_key(str(p.entryId)):

                        # tokenize publications
                        # get topic probabilities
                        # get distance to seed publications for each linked publication

                        # ----- tokenize - begin -----------------------------------
                        tokens = []

                        # keywords
                        [ tokens.append(s.topicName) for s in p.topics ]

                        # paper text
                        words=p.entryTitle.encode("utf-8") + ". "+ p.entryAbstract.encode("utf-8")
                        _tokens, _stopwords, _unknownwords = tokenizer.tokens(words)
                        [tokens.append(tk) for tk in _tokens]
                        # ----- tokenize - end -------------------------------------

                        # apply topic model
                        topics = model.topics_from_doc(tokens)

                        distanceToSeed=1000.0
                        for seedId in seedIds:
                            d = difference(topics, fullDictionary[str(seedId)]['topics'])
                            if d<distanceToSeed:
                                distanceToSeed = d

                        # 
                        fullDictionary[str(p.entryId)] = {
                            'entryId': p.entryId,
                            'url':p.entryURL,
                            'text': words,
                            'keywords':";".join([ s.toCSV() for s in p.topics]),
                            'tokens':tokens,
                            'referencesTo':p.referencesTo,
                            'referencedBy':[],
                            'ECC':p.ECC,
                            'year':p.entryPublished,
                            'topics':topics.tolist(),
                            'distanceToSeed':distanceToSeed
                        }
                        #distances.append(distanceToSeed)
                        print "indexing: id",p.entryId, " dist=",distanceToSeed, " ECC=",p.ECC," year=",p.entryPublished," title=",p.entryTitle

            
                # append top X% of linked publications to nextLevelQueue if they are not in registry
                # save top X% of linked publications to file
                print "maxDistance=", maxDistance
                for p in linkedPublications:
                    
                    # print "testing ",p.entryId
                    
                    topicIsValid = True
                    for t in p.topics:
                        if  t.topicId in msAcademicExcludeTopicsIds:
                            topicIsValid = false;
                    
                    if topicIsValid and fullDictionary[str(p.entryId)]['distanceToSeed']<=maxDistance and p.entryId not in indexedDocs :
                        # to get referencing publications at next level
                        nextLevelQueue.put(p.entryId)
                        # to get referenced publications at next level
                        for docId in p.referencesTo:
                            nextLevelQueue.put(docId)
                        writer.writerow(flatten(fullDictionary[str(p.entryId)]))
                        acceptedDocs.add(p.entryId)
                        msg=("+++++accepted", len(acceptedDocs), 'of', len(indexedDocs),"id=",p.entryId, "dist=",fullDictionary[str(p.entryId)]['distanceToSeed'], " ECC=",p.ECC," year=",p.entryPublished," title=",p.entryTitle)
                    else:
                        msg=("-----rejected", len(acceptedDocs), 'of', len(indexedDocs)," id=",p.entryId, " dist=",fullDictionary[str(p.entryId)]['distanceToSeed'], " ECC=",p.ECC," year=",p.entryPublished," title=",p.entryTitle)

                    print msg
                    logMessages.append("\t".join(map(str, msg)))
                    
                    if len(logMessages)>500:
                        file = open(logFile,"a")
                        file.write("\n".join(logMessages)) 
                        file.write("\n") 
                        file.close() 
                        logMessages=[]

                    # mark publication as indexed
                    indexedDocs.add(p.entryId)

                file = open(logFile,"a")
                file.write("\n".join(logMessages)) 
                file.write("\n") 
                file.close() 
                logMessages=[]

                linkedPublications =[]
                print "length-of-nextLevelQueue =", nextLevelQueue.qsize()

        
        
        if nextLevelQueue.qsize()>200000:
            break;
        currentLevelQueue=nextLevelQueue
        #print "length of nextLevelQueue =", len(nextLevelQueue)
    
    
    
    
    


    csvOutputFile.close()
    return
    
    
    
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
