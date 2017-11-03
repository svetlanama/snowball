import sys
sys.path.insert(0, '..')

import ConfigParser
import csv
import numpy
import ConfigParser
import topicmodel
import time

def main():

    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')
    Hmax = config.getfloat('main', 'Hmax')

    io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)

    # read wordDictionary
    wordDictionary = io.load_csv_as_dict('out-word-dictionary-rare-words-excluded.csv')
    #print wordDictionary
    
    model.set_word_dictionary(wordDictionary)
    #print model.wordDictionary
    #return


    wwcovar = numpy.load(dataDir+'/tmp-joint-probabilities.npy')

    
    #print wordDictionary
    #print wordDictionaryInverse
    #return
    
    stopwords = model.stopwords(wwcovar, Hmax)
    print "stopwords=\n",stopwords
    io.save_dict_as_csv('out-stopwords.csv', stopwords)
    return



if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
