import sys
reload(sys)  
#sys.path.insert(0, '..')
sys.setdefaultencoding('utf8')

import ConfigParser
import time
import topicmodel

def main():

    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')
    alpha = config.getfloat('main', 'alpha')



    io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)
    
    
    # read wordDictionary
    wordDictionary = io.load_csv_as_dict('out-word-dictionary.csv')
    #print wordDictionary
    
    model.set_word_dictionary(wordDictionary)
    #print model.wordDictionary
    #return

    rarewords = model.rarewordsMemoryOptimal('tmp-all-paper-tokens.csv', alpha,'+','.')

    print rarewords
    io.save_dict_as_csv('out-rarewords.csv', rarewords)
    
    # exclude rare words from wordDictionary
    reducedWordDictionary = model.reduced_dictionary(wordDictionary, {}, rarewords)
    io.save_dict_as_csv('out-word-dictionary-rare-words-excluded.csv', reducedWordDictionary)
    
    print "Dictionary size:", len(wordDictionary), " => ", len(reducedWordDictionary)

    return



if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
