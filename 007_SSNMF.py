import ConfigParser
import numpy
import time
import topicmodel

#
# gradient descent method for SNMF
# the best variant
# 
def main():
    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    Pmax = config.getint('main', 'Pmax')
    dataDir = config.get('main', 'dataDir')
    lam = config.getfloat('main', 'lambda')

    # io = topicmodel.io(dataDir)
    model = topicmodel.model(dataDir)

    jProbReduced = numpy.load(dataDir + '/tmp-joint-probability-reduced.npy')
    print "len(wwcovarReduced)=",len(jProbReduced)
    
    H = model.sparse_snmf(jProbReduced, Pmax, {'eta': 0.1, 'beta': 0.99, 'beta2': 1.000, 'maxError': 1e-7, 'maxIterations':2000, 'lambda':lam})

    numpy.save(dataDir + '/out-SSNMFResult.npy', H)
    
    TM = model.model_from_factor(H)
    numpy.save(dataDir + '/out-TopicModel.npy', TM)
    
    return 
    '''







    '''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0

