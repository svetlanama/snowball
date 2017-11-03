import ConfigParser
import numpy
import time
import topicmodel

print "Calculating topic coherence"

def main():
    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    nTopWords = config.getint('main', 'nCoherenceWords')
    dataDir = config.get('main', 'dataDir')

    io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)

    wwcovarReduced = numpy.load(dataDir + '/tmp-joint-probability-reduced.npy')
    # print wwcovarReduced
    # return




    H = numpy.load(dataDir + '/out-SSNMFResult.npy')
    nTopics = len(H[0])
    nWords = len(H)

    # {'P':P, 'N':N}
    topicModel = numpy.load(dataDir + '/out-TopicModel.npy')
    topicModel = topicModel.item()
    

    
    # read wordDictionary
    wordDictionary = io.load_csv_as_dict('out-word-dictionary-reduced.csv')
    model.set_word_dictionary(wordDictionary)
    # print model.wordDictionaryInverse
    # return
    
    # use wwcovarReduced to get word probability
    wordProbability = model.word_probability(wwcovarReduced)
    # print wordProbability
    # return
    
    # coherence normalization constant
    eps = 0.0001

    coherence = []
    for iTopic in xrange(0, nTopics):
        # calculate coherence
        
        print "topic ", iTopic

        # get top words ids
        topicWordWeights = topicModel['P'].T[iTopic]
        #print topicWordWeights
        #print len(topicWordWeights)
        #return
        sortedTopicWordWeights = numpy.sort(topicWordWeights)
        sortedTopicWordWeights = sortedTopicWordWeights[::-1]
        minAllowedWordWeight = sortedTopicWordWeights[nTopWords]
        topWordIds = []
        for wId in xrange(0, nWords):
            if topicWordWeights[wId] > minAllowedWordWeight:
                topWordIds.append(wId)
        # print topWordIds
        # return
        # show top topic words along with their weights
        topWords=[]
        for wId in topWordIds:
            topWords.append([model.wordDictionaryInverse[wId], topicWordWeights[wId]])
            # print model.wordDictionaryInverse[wId],"+", topicWordWeights[wId]
        # custom words sorting
        topWords = sorted(topWords, key=lambda row: -row[1])
        for row in topWords:
            print row[0],"+",row[1]
        # return


        # use Normalized Pointwise Mutual Information
        Cuci = 0
        for iWord in topWordIds:
            for jWord in topWordIds:
                if jWord > iWord:
                    a1 = numpy.log(wwcovarReduced[iWord][jWord] + eps)
                    a2 = numpy.log(wordProbability[iWord] * wordProbability[jWord])
                    Cuci = Cuci - (1 - a2 / a1) 

        Cuci = Cuci * 2.0 / (nTopWords * (nTopWords-1))
        coherence.append(Cuci)
        print Cuci, "\n\n\n"

    print "coherence by topic="
    print coherence
    
    # get average coherence
    avgCoherence = 0
    nSignificantTopics=0
    for c in coherence:
        if c>0:
            avgCoherence = avgCoherence + c 
            nSignificantTopics += 1
    avgCoherence = avgCoherence / nSignificantTopics
    print "avgCoherence=", avgCoherence
        
        
    return 
    


if __name__ == "__main__":
    
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0

