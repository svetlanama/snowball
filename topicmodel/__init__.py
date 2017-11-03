import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import numpy
import random
#import tables
from nltk.corpus import stopwords


#    validPOSTags = {'NNP':True, 'JJ':True, 'NN':True, 'NNS':True, 'JJS':True, 'JJR':True, 'NNPS':True};
#    tester = re.compile('^[a-zA-Z]+$')
#    wordDictionary={}

class CustomTokenizer:
    def __init__(self):
        self.validPOSTags = {}
        self.stemmer = False # PorterStemmer()
        self.tester = False  # re.compile('^[a-zA-Z]+$')
        self.wordDictionary = {}
        self.stop = set([])

    def tokens(self, string):
        print string
        text = nltk.word_tokenize(string)
        taggedWords = nltk.pos_tag(text)
        words = []
        for tw in taggedWords:
            #print tw
            if(self.validPOSTags.has_key(tw[1])):
                theWord = tw[0].lower()
                # print theWord, tester.match(theWord)

                if (self.tester.match(theWord) and theWord not in self.stop):
                    try:
                        theWord = self.stemmer.stem(tw[0].lower()).encode('utf-8')
                    except IndexError:
                        continue

                    if(not self.wordDictionary.has_key(theWord)):
                        self.wordDictionary[theWord] = len(self.wordDictionary);

                    if(self.wordDictionary.has_key(theWord)):
                        words.append(theWord)
        return words
    
    
'''



'''
class io:
    def __init__(self, outputDir):
        self.outputDir = outputDir
    
    def save_dict_as_csv(self, filename, aDictionary):
        keys = aDictionary.keys()
        fieldnames = ['key', 'value']
        dictOutputFile = open(self.outputDir + '/' + filename, 'w')
        writer = csv.DictWriter(dictOutputFile, fieldnames=fieldnames, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)
        writer.writeheader()

        for k in aDictionary.keys():
            writer.writerow({'key':k, 'value':aDictionary[k]})

        dictOutputFile.close()
        
    def load_csv_as_dict(self, filename):
        csvInputFile = open(self.outputDir + '/' + filename, 'r')
        csvreader = csv.DictReader(csvInputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

        wordDictionary = {}
        wordDictionaryInverse = {}
        for dat in csvreader:
            wordDictionary[dat['key']] = dat['value']
            #wordDictionaryInverse[dat['value']] = dat['key']
        csvInputFile.close();
        
        return wordDictionary

        #wordDictionarySize = len(wordDictionary)

'''



'''
class model:
    def __init__(self, outputDir):
        self.outputDir = outputDir
        self.wordDictionary = {}
        self.wordDictionarySize = 0
        self.wordDictionaryInverse = {}
        self.wwcovar = []
        self.topic_model = []

    '''
    
    
    set_word_dictionary
    '''
    def set_word_dictionary(self, wordDictionary):
        self.wordDictionarySize = len(wordDictionary)
        self.wordDictionaryInverse = {}
        self.wordDictionary = {}
        for key in wordDictionary.keys():
            self.wordDictionary[key] = int(wordDictionary[key])
            self.wordDictionaryInverse[int(wordDictionary[key])] = key
        #print self.wordDictionaryInverse
        return
        
    '''
    
    
    coccurences
    '''
    def coccurences(self, paperTokensCsvFile, word_separator=' ',sentence_separator='.'):

        csvInputFile = open(self.outputDir + '/' + paperTokensCsvFile, 'r')
        csvreader = csv.DictReader(csvInputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

        # print (long(self.wordDictionarySize), long(self.wordDictionarySize) )
        # wwcovar = numpy.memmap(self.outputDir + '/wwcovar.swap', dtype='int', mode='w+', shape=(50000, 50000 ))
        # wwcovar = numpy.memmap(self.outputDir + '/wwcovar.swap', dtype='float32', mode='w+', shape=(self.wordDictionarySize, self.wordDictionarySize ))
        # return 
        wwcovar = numpy.zeros((self.wordDictionarySize, self.wordDictionarySize), dtype=numpy.int)
        print "self.wordDictionarySize=",self.wordDictionarySize
        #wwcovar = numpy.memmap(self.outputDir + '/wwcovar.swap', dtype='int', mode='w+', shape=( int(self.wordDictionarySize), int(self.wordDictionarySize) ))
        #wwcovar = numpy.memmap(self.outputDir + '/wwcovar.swap', dtype='float32', mode='w+', shape=( int(self.wordDictionarySize), int(self.wordDictionarySize) ))
        #wwcovar = numpy.memmap('/media/dobro/RAM/wwcovar.swap', dtype='float32', mode='w+', shape=(self.wordDictionarySize, self.wordDictionarySize ))
        
        
        norma = 0.0

        random.seed()
        for dat in csvreader:
            sentences = dat['tokens'].split(sentence_separator)
            for sentence in sentences:
                words = sentence.split(word_separator)
                #print words
                # iterate over words in the group
                for i in xrange(0, len(words)):
                    w1 = words[i]
                    for j in xrange(i + 1, len(words)):
                        w2 = words[j]

                        if(self.wordDictionary.has_key(w1) and self.wordDictionary.has_key(w2)):
                            # print w1, w2
                            w1position = int(self.wordDictionary[w1])
                            w2position = int(self.wordDictionary[w2])
                            
                            if random.random() < 0.0001 :
                               print "update", w1position, w2position
                               # , type(w1position), type(w2position)

                            wwcovar[w1position][w2position] = wwcovar[w1position][w2position] + 1
                            wwcovar[w2position][w1position] = wwcovar[w1position][w2position]
                            norma += 2
                        #else:
                        #    print "invalid pair ", w1, w2

        print "Counting finished"
        csvInputFile.close();

        norma = 1.0 / norma
        print norma

        #for i in xrange(0, self.wordDictionarySize):
        #    for j in xrange(i, self.wordDictionarySize):
        #        wwcovar[i][j] = wwcovar[i][j] * norma
        #        wwcovar[j][i] = wwcovar[i][j]
        #        #if(wwcovar[i][j]>0):
        #        #   print i,j,wwcovar[i][j]
        #print "Normalization finished"

        #        norma = 0.0
        #        for i in xrange(0, self.wordDictionarySize):
        #            for j in xrange(0, self.wordDictionarySize):
        #                norma += wwcovar[i][j]
        #        print norma
        #        print "Normalization tested"
        
        #return [wwcovar, norma]
        return wwcovar * norma
    
    
    
    

    
    '''
    
    
    word_probability
    '''
    def word_probability(self, wwcovar):

        wordProbability = numpy.zeros(self.wordDictionarySize)

        for i in xrange(0, self.wordDictionarySize):
            for j in xrange(0, self.wordDictionarySize):
                wordProbability[i] = wwcovar[i][j] + wordProbability[i]
        # print wordProbability
        return wordProbability
    
    
    '''
    
    
    stopwords
    '''
    def stopwords(self, wwcovar, Hmax):
        wordProbability = self.word_probability(wwcovar)
    
        entropy = numpy.zeros(self.wordDictionarySize)
        for i in xrange(0, self.wordDictionarySize):
            if wordProbability[i] > 0:
                z = 1.0 / wordProbability[i]
                for j in xrange(0, self.wordDictionarySize):
                    if (wwcovar[i][j] > 0):
                        term = wwcovar[i][j] * z
                        entropy[i] -= term * numpy.log(term)



        # get maximal allowed entropy value    
        sortedEntropy = numpy.sort(entropy)
        sortedEntropy = sortedEntropy[::-1]
        print "sortedEntropy=\n",sortedEntropy.tolist()
    
        numberOfWords = len(sortedEntropy)
        entropyMaxValuePos = int(numberOfWords * Hmax) - 1
        if entropyMaxValuePos < 0:
            entropyMaxValuePos = 0
        print "entropyMaxValuePos=", entropyMaxValuePos
        entropyMaxValue = sortedEntropy[entropyMaxValuePos]

        print "entropyMaxValue=", entropyMaxValue

        # stop-words are ones having large entropy
        stopwords = {}
        for i in xrange(0, self.wordDictionarySize):
            if(entropy[i] > entropyMaxValue):
                # stopwords[i] = self.wordDictionaryInverse[i]
                stopwords[self.wordDictionaryInverse[i]] = i
                print i, self.wordDictionaryInverse[i], entropy[i]
                #print i, entropy[i]
        return stopwords
    
    
    
    '''
    
    
    rare words
    '''
    def rarewords(self, wwcovar, alpha):

        wordProbability = self.word_probability(wwcovar)

        # get maximal allowed entropy value    
        sortedWordProbability = numpy.sort(wordProbability)
        # print sortedWordProbability.tolist()


        summa = 0
        i = -1
        while summa <= alpha:
            i = i + 1
            summa = summa + sortedWordProbability[i]
        probabilityMinValue = sortedWordProbability[i]
        print "probabilityMinValue=", probabilityMinValue



        # stop-words are ones having large entropy
        rarewords = {}
        iMax = len(sortedWordProbability)-1
        for i in xrange(0, iMax):
            if(wordProbability[i] <= probabilityMinValue):
                # rarewords[i] = wordDictionaryInverse[i]
                rarewords[self.wordDictionaryInverse[i]] = i
                print i, self.wordDictionaryInverse[i], wordProbability[i]
        
        return rarewords
    
    
    

    '''
    
    
    rare words
    
    '''
    def rarewordsMemoryOptimal(self, paperTokensCsvFile, alpha, word_separator=' ',sentence_separator='.'):

        csvInputFile = open(self.outputDir + '/' + paperTokensCsvFile, 'r')
        csvreader = csv.DictReader(csvInputFile, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

        wordProbability = numpy.zeros(self.wordDictionarySize)

        random.seed()
        norma = 0
        for dat in csvreader:
            sentences = dat['tokens'].split(sentence_separator)
            for sentence in sentences:
                words = sentence.split(word_separator)
                #print words
                # iterate over words in the group
                for i in xrange(0, len(words)):
                    w1 = words[i]
                    if self.wordDictionary.has_key(w1):
                        w1position = int(self.wordDictionary[w1])
                        wordProbability[w1position] += 1
                        norma += 1
        norma = 1.0 / norma
        print norma

        wordProbability = wordProbability * norma

        print "Counting finished"
        csvInputFile.close();

        # get maximal allowed entropy value    
        sortedWordProbability = numpy.sort(wordProbability)
        # print sortedWordProbability.tolist()


        summa = 0
        i = -1
        while summa <= alpha:
            i = i + 1
            summa = summa + sortedWordProbability[i]
        probabilityMinValue = sortedWordProbability[i]
        print "probabilityMinValue=", probabilityMinValue


        rarewords = {}
        iMax = len(sortedWordProbability)-1
        for i in xrange(0, iMax):
            if(wordProbability[i] <= probabilityMinValue):
                # rarewords[i] = wordDictionaryInverse[i]
                rarewords[self.wordDictionaryInverse[i]] = i
                print i, self.wordDictionaryInverse[i], wordProbability[i]
        
        return rarewords
    
    '''
    
    
    
    reduced dictionary
    '''
    def reduced_dictionary(self, wordDictionary, stopwords, rarewords):
        reducedWordDictionary = {}
        iw = 0
        for word in wordDictionary.keys():
            if  not (stopwords.has_key(word) or rarewords.has_key(word)):
                reducedWordDictionary[word] = iw
                iw = iw + 1

        return reducedWordDictionary
    
    
    '''
    
    
    
    symmetric nonnegative matrix factorization
    projected gradient descent
    '''
    def snmf(self, wwcovar, Pmax, parameters):
        # parameters['eta'] = 0.1
        # parameters['beta'] = 0.9
        # parameters['beta2'] = 1.001
        # parameters['maxError'] = 1e-10

        # 'maxIterations':1000
        if parameters.has_key('maxIterations'):
            maxIterations = int(parameters['maxIterations'])
        else:
            maxIterations = 200
        # ================= SNMF = BEGIN ===========================================
        # SNMF dimensions    
        # print Pmax, len(wwcovarReduced)
        # return 
        nWords = len(wwcovar)
        nTopics = Pmax
        print nWords, nTopics

        # ranges
        x1range = xrange(0, nWords) 
        x2range = xrange(0, nTopics) 

        if parameters.has_key('H'):
            H = parameters['H']
        else:
            H = numpy.zeros((nWords, nTopics))
            # initial random values
            for i in x1range:
                for j in x2range:
                    H[i][j] = random.random()

        d1 = -1
        d2 = -1
        cnt = 1
        for iteration in xrange(0, maxIterations):

            diff = H.dot(H.T) - wwcovar
            # print diff

            grad = diff.dot(H)
            #print grad
            maxGrad = 0
            for x1 in x1range:
                for x2 in x2range:
                    if maxGrad < abs(grad[x1][x2]):
                        maxGrad = abs(grad[x1][x2])


            d = parameters['eta'] / maxGrad
            #d=eta
            for x1 in x1range:
                for x2 in x2range:
                    H[x1][x2] = H[x1][x2] - d * grad[x1][x2]
                    if H[x1][x2] < 0:
                        H[x1][x2] = 0

            if d2 > d1:
                parameters['eta'] = parameters['eta'] * parameters['beta']
            else:
                parameters['eta'] = parameters['eta'] * parameters['beta2']
            # print H
            if d2 > d1:
                parameters['eta'] = parameters['eta'] * parameters['beta']
            else:
                parameters['eta'] = parameters['eta'] * parameters['beta2']


            error = numpy.linalg.norm(diff, ord='fro')
            d1 = d2
            d2 = error

            if cnt >= 10:
                print iteration,  ' eta=', parameters['eta'], "error=", error, " sparsity=", self.sparsity(H)
                cnt = 1
            else:
                cnt = cnt + 1
                
            if parameters['maxError'] > error:
            #if parameters['maxError'] > parameters['eta']:
                break


        print "error=", numpy.linalg.norm(H.dot(H.T) - wwcovar, ord='fro')
        
        return H
    '''




    '''
    def sparsity(self, H):
        n1 = len(H)
        n2 = len(H[0])
        n = n1 * n2
        L2 = 0
        L1 = 0
        for x1 in xrange(0, n1):
            for x2 in xrange(0, n2):
                L1 = L1 + H[x1][x2]
                L2 = L2 + H[x1][x2] * H[x1][x2]

        return numpy.sqrt(n) / (numpy.sqrt(n) - 1) - 1.0 / (numpy.sqrt(n) - 1) * L1 / numpy.sqrt(L2)
    
    

    '''
    
    
    '''
    def D(self, H, a, b):
        n1 = len(H)
        n2 = len(H[0])
        L2 = 0
        L1 = 0
        for x1 in xrange(0, n1):
            for x2 in xrange(0, n2):
                L1 = L1 + H[x1][x2]
                L2 = L2 + H[x1][x2] * H[x1][x2]
        S1 = 0
        S2 = 0
        for k in xrange(0, n1):
            S1 = S1 + H[k][a]
            S2 = S2 + H[k][a] * H[k][b]

        return - 1.0 / (numpy.sqrt(n1 * n2) - 1) * (S1 * numpy.power(L2, -0.5) - L1 * S2 * numpy.power(L2, -1.5))

    '''
    
    
    
    symmetric nonnegative matrix factorization
    projected gradient descent
    '''
    def sparse_snmf(self, wwcovar, Pmax, parameters):
        # parameters['eta'] = 0.1
        # parameters['beta'] = 0.9
        # parameters['beta2'] = 1.001
        # parameters['maxError'] = 1e-10
        # parameters['lambda'] = 

        # 'maxIterations':1000
        if parameters.has_key('maxIterations'):
            maxIterations = int(parameters['maxIterations'])
        else:
            maxIterations = 200
        # ================= SNMF = BEGIN ===========================================
        # SNMF dimensions    
        # print Pmax, len(wwcovarReduced)
        # return 
        H = numpy.zeros((len(wwcovar), Pmax))
        nWords = len(H)
        nTopics = len(H[0])
        print nWords, nTopics

        # ranges
        x1range = xrange(0, nWords) 
        x2range = xrange(0, nTopics) 

        # initial random values
        for i in x1range:
            for j in x2range:
                H[i][j] = random.random()

        d1 = -1
        d2 = -1
        cnt = 1
        # L = float(parameters['lambda'])
        
        avgError = 0
        
        for iteration in xrange(0, maxIterations):

            diff = H.dot(H.T) - wwcovar
            # print diff


            grad = diff.dot(H) #+ L 
            #print grad
            maxGrad = 0
            for x1 in x1range:
                for x2 in x2range:
                    if maxGrad < abs(grad[x1][x2]):
                        maxGrad = abs(grad[x1][x2])

            if maxGrad < parameters['maxError']:
                break


            d = parameters['eta'] / maxGrad
            #d=eta
            for x1 in x1range:
                for x2 in x2range:
                    H[x1][x2] = H[x1][x2] - d * grad[x1][x2]
                    if H[x1][x2] < 0:
                        H[x1][x2] = 0

            if d2 > d1:
                parameters['eta'] = parameters['eta'] * parameters['beta']
            else:
                parameters['eta'] = parameters['eta'] * parameters['beta2']


            error = numpy.linalg.norm(diff, ord='fro')
            d1 = d2
            d2 = error

            if cnt >= 10:
                print iteration,  ' eta=', parameters['eta'], "error=", error, " sparsity=", self.sparsity(H)
                cnt = 1
            else:
                cnt = cnt + 1
                

            if parameters['maxError'] > abs(error-avgError):
                break

            avgError = 0.9 * avgError + 0.1 * error

        
        print "error=", numpy.linalg.norm(H.dot(H.T) - wwcovar, ord='fro')
        
        return H
    '''
    
    
    normalization
    
    
    '''
    def model_from_factor(self, H):
        
        nWords = len(H)
        nTopics = len(H[0])
        
        N = numpy.zeros(nTopics)
        P = numpy.zeros((nWords, nTopics))

        for iTopic in xrange(0, nTopics):

            # c1 = H.T[iTopic]

            norm = 0
            for p in H.T[iTopic]:
                norm = norm + p

            print "topic" + str(iTopic) + " ", norm * norm

            if norm > 0:
                for i in xrange(0, nWords):
                    P.T[iTopic][i] = H.T[iTopic][i] / norm

            N[iTopic] = norm * norm
            
        return {'P':P, 'N':N}
    
    
    '''
    
    
    
    
    '''
    def load_topic_model(self, wwcovar, topic_model):
        
        # covariance
        self.wwcovar = wwcovar
        
        # topic model
        self.topic_model = topic_model
        
        # topic probability
        self.pt = topic_model['N']
        
        # word probability
        self.pw = numpy.zeros(self.wordDictionarySize)
        for i in xrange(0, len(self.wwcovar)):
            s = 0
            for j in xrange(0, len(self.wwcovar)):
                s = s + self.wwcovar[i][j]
            self.pw[i] = s
        print self.pw
        #return

        self.pwt = topic_model['P']
        self.nWords = len(self.pwt)
        self.nTopics = len(self.pwt[0])
        print "nWords=", self.nWords, " nTopics= ", self.nTopics
        # return

        self.ptw = numpy.zeros((self.nTopics, self.nWords))    # numpy.save('out/TopicModel.npy', {'H':H, 'N':N})

        for iWord in xrange(0, self.nWords):
            for iTopic in xrange(0, self.nTopics):
                if self.pw[iWord] > 0:
                    self.ptw[iTopic][iWord] = self.pwt[iWord][iTopic] * self.pt[iTopic] / self.pw[iWord]

        # print ptw
        # return

    '''
    
    
    
    
    '''
    def topics_from_doc(self, words):

        pwd = numpy.zeros(self.nWords)
        wordTotal = len(words)

        for word in words:
            # print word
            if self.wordDictionary.has_key(word):
                # print word, self.wordDictionary[word]
                iWord = self.wordDictionary[word]
                if iWord < self.nWords:
                    pwd[iWord] = pwd[iWord] + 1
                else:
                    print "word, iWord = ", word, iWord
        # return
        # print wordTotal, pwd.tolist()
        # return
        
        norm = 1.0 / max(wordTotal,1)
        for i in xrange(0, self.nWords):
            pwd[i] = pwd[i] * norm
        
        #print wordTotal, pwd.tolist()
        #return
    
        ptd = numpy.zeros(self.nTopics) 
        for iTopic in xrange(0, self.nTopics):
            s = 0
            for iWord in xrange(0, self.nWords):
                s = s + self.ptw[iTopic][iWord] * pwd[iWord]
            #print ptw[iTopic].tolist()
            #print pwd.tolist()
            #print "iTopic=", iTopic, " s=",s
            #print "=================="
            
            ptd[iTopic] = s

        return ptd

