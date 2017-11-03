import sys
sys.path.insert(0, '..')

import ConfigParser
import csv
import numpy
import time
import topicmodel

def main():

    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    dataDir = config.get('main', 'dataDir')

    io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)
    
    
    
    # read wordDictionary
    wordDictionary = io.load_csv_as_dict('out-word-dictionary.csv')
    #print wordDictionary
    
    model.set_word_dictionary(wordDictionary)
    # print model.wordDictionary
    # return

    # read stopwords
    stopwords=io.load_csv_as_dict('out-stopwords.csv')
    print stopwords
    #return 


    # read rarewords
    rarewords=io.load_csv_as_dict('out-rarewords.csv')
    print rarewords
    
    
    reducedWordDictionary = model.reduced_dictionary(wordDictionary, stopwords, rarewords)
    reducedWordDictionarySize = len(reducedWordDictionary)
    print len(wordDictionary), "=>",reducedWordDictionarySize
    io.save_dict_as_csv('out-word-dictionary-reduced.csv', reducedWordDictionary)
    
    
    model.set_word_dictionary(reducedWordDictionary)
    

    wwcovarReduced=model.coccurences('tmp-all-paper-tokens.csv','+','.')
    numpy.save(dataDir+'/tmp-joint-probability-reduced.npy', wwcovarReduced)

    wordProbability = model.word_probability(wwcovarReduced)
    numpy.save(dataDir+'/tmp-word-probability-reduced.npy', wordProbability)
    
    return




if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0

