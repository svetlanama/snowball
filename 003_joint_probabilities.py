import sys
sys.path.insert(0, '..')


import numpy
import time
import ConfigParser
import topicmodel

def main():

    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    dataDir = config.get('main', 'dataDir')
    
    
    io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)
    
    wordDictionary = io.load_csv_as_dict('out-word-dictionary-rare-words-excluded.csv')
    model.set_word_dictionary(wordDictionary)
    # print wordDictionary
    # return

    wwcovar=model.coccurences('tmp-all-paper-tokens.csv','+','.')
    numpy.save(dataDir + '/tmp-joint-probabilities.npy', wwcovar)
    return

if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
