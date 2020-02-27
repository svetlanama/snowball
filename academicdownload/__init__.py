import base64
import httplib
import json
import re
import urllib
import topicmodel
import numpy
import csv
from nltk.stem.porter import *
from nltk.corpus import stopwords
import os.path

class Entry:
    def __init__(self):
        self.entryId = ''
        self.entryTitle = ''
        self.entryURL = ''
        self.entryAbstract = ''
        self.entryPublished = ''
        self.authors = []
        self.topics = []
        self.referencesTo = []
        self.referencedBy = []
        self.level = ''
        self.ECC = 0
		# self.entryDOI = ''

    def clear(self, x):
        return re.sub(r"\\t|\\n|\\r", "", x)

    def toCsv(self):
        sb = [];
        sb.append(self.clear(str(self.entryId)).encode('utf-8'))        # 0
        sb.append(self.clear(self.entryTitle).encode('utf-8'))          # 1
        sb.append(self.clear(self.entryURL).encode('utf-8'));           # 2
        sb.append(self.clear(str(self.entryPublished)).encode('utf-8')) # 3
        sb.append(self.clear(self.entryAbstract).encode('utf-8'))       # 4

        sb.append(";".join([a.toCSV() for a in self.authors]))          # 5 list of authors

        sb.append(";".join([a.toCSV() for a in self.topics]))           # 6 list of topics

        sb.append(";".join([str(a) for a in self.referencesTo]))        # 7 list of refereces

        if len(self.referencedBy) > 0:
            sb.append(";".join([str(a) for a in self.referencedBy]))    # 8 list of backrefereces
        else:
            sb.append("")                                               # 8 list of backrefereces

        sb.append(str(self.ECC))
	    # sb.append(self.clear(self.entryDOI).encode('utf-8'));   		# 10  doi
        return "\t".join(sb)
'''




'''
def entryFromCsv(csv):

    if (not isinstance(csv, str) or len(csv) == 0):
        return null

    cols = csv.split("\t")

    en = Entry()
    en.entryId = cols[0]
    en.entryTitle = cols[1]
    en.entryURL = cols[2]
    en.entryPublished = cols[3]
    en.entryAbstract = cols[4]
    en.authors = authorListFromCsv(cols[5].split(";"))
    en.topics = topicListFromCsv(cols[6].split(";"))
    if (len(cols) > 7):
        en.referencesTo = cols[7].split(";")
    else:
        en.referencesTo = []


    if (len(cols) > 8):
        en.referencedBy = cols[8].split(";")
    else:
        en.referencedBy = []

    if (len(cols) > 9):
        en.ECC = int(cols[9])
    else:
        en.ECC = 0

	# en.entryDOI = cols[10]

    return en






'''




'''
class Author:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.affiliation = ''
        self.affiliationId = ''

    def toCSV(self):
        sb = []
        sb.append(str(self.id));
        sb.append(self.name.encode('utf-8'));
        sb.append(str(self.affiliationId));
        sb.append(self.affiliation.encode('utf-8'));

        return "@".join(sb);



'''




'''
def authorListFromCsv(csvList):
    lst = []
    for csv in csvList:
        if len(csv) > 0:
            lst.append(authorFromCsv(csv))
    return lst


'''




'''
def authorFromCsv(csv):
    au = Author()

    parts = csv.split("@");
    # print parts
    # return
    au.id = parts[0];
    au.name = parts[1];
    if len(parts) > 2:
        au.affiliation = parts[2]
    else:
        au.affiliation = ""

    if len(parts) > 3:
        au.affiliationId = parts[3]
    else:
        au.affiliationId = ""

    return au;

'''




'''
class Topic:

    def __init__(self):
        self.topicId = ''
        self.topicName = ''

    def toCSV(self):
        sb = []
        sb.append(str(self.topicId))
        sb.append(self.topicName.encode('utf-8'))
        return "@".join(sb)



'''




'''
def topicListFromCsv(csvList):
    lst = []
    for csv in csvList:
        if len(csv) > 0:
            lst.append(topicListFromCsv(csv))
    return lst

'''




'''
def topicListFromCsv(csv):
    to = Topic()
    parts = csv.split("@");
    to.topicId = parts[0]
    to.topicName = parts[1]
    return to




'''




'''
class Api:

    def __init__(self, subscriptionKey):
        self.subscriptionKey = subscriptionKey

    '''





    '''
    def loadList(self, f):
        q = []

        #out-invalid.csv
        if os.path.isfile(f) :
            thefile = open(f, 'r')
            data = thefile.read()
            thefile.close();

            a = data.split("\n")
            for row in a:
                rw = row.strip(" \n\t")
                if len(rw) > 0:
                    tmp = rw.split("#")
                    q.append(tmp[0])
        return q
    '''





    '''
    def loadEntries(self, f):
        q = []
        thefile = open(f, 'r')
        data = thefile.read()
        thefile.close();

        a = data.split("\n")
        for row in a:
            if len(row) > 0:
                q.append(entryFromCsv(row.strip(' ')))
        return q

    '''




    '''
    def loadByIds(self, entryIds, msAcademicIncludeTopicsIds):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["Id=" + regex.sub('', str(int(x))) for x in entryIds])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in msAcademicIncludeTopicsIds])) + ")"
        res = self.callApi("and(" + sbIds + ", " + sbFIds + ")", 'Id,Ti,Y,RId,F.FN,F.FN,F.FId,AA.AuId,AA.AuN,AA.AfN,AA.AfId,E,ECC')
        #,E
        return res
    '''





    '''
    def loadByRIds(self, entryIds, msAcademicIncludeTopicsIds):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["RId=" + regex.sub('', str(x)) for x in entryIds])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in msAcademicIncludeTopicsIds])) + ")"
        return self.callApi("and(" + sbIds + ", " + sbFIds + ")", 'Id,Ti,Y')
    '''





    '''
    def loadByRIdsExtended(self, entryIds, msAcademicIncludeTopicsIds):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["RId=" + regex.sub('', str(x)) for x in entryIds])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in msAcademicIncludeTopicsIds])) + ")"
        return self.callApi("and(" + sbIds + ", " + sbFIds + ")", 'Id,Ti,Y,RId,F.FN,F.FN,F.FId,AA.AuId,AA.AuN,AA.AfN,AA.AfId,E,ECC')
    '''





    '''
    def callApi(self, expr, attributes):
        res = []
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.subscriptionKey,
        }
        # print "self.subscriptionKey="+self.subscriptionKey+';'
        # print expr
        params = urllib.urlencode({
                                  # Request parameters
                                  'expr': expr,
                                  'complete': '0',
                                  'count': '1000',
                                  'offset': '0',
                                  'timeout': '60',
                                  'model': 'latest',
                                  'attributes':attributes
                                  })
        # print params

        try:
            # print(params)
            # https://                      westus.api.cognitive.microsoft.com
            #api.labs.cognitive.microsoft.com
            conn = httplib.HTTPSConnection('api.labs.cognitive.microsoft.com')
            conn.request("GET", "/academic/v1.0/evaluate?" + params, "", headers)
            response = conn.getresponse()
            # print response
            jsonString = response.read()
            print jsonString
            data = json.loads(jsonString)
            #print(data['entities'])

            for entity in data['entities']:
                en = self.loadEntity(entity)
                res.append(en)
            # print(data)
            conn.close()
        except Exception as e:
            #print("[Errno {0}] {1}".format(e.errno, e.strerror))
            print e

        return res
    '''



    '''
    def loadEntity(self, entity):
        res = Entry();
        #"entities":
        #[
        #{
        #  "logprob":-15.670,
        #  "Id":2001082470,
        #  "Ti":"finding scientific topics",
        #  "Y":2004,
        #  "RId":[1574901103,33994038,1666636243,2069739265,2104924585,2534302,204170073,2165554837],
        #  "AA":[{"AuN":"thomas l griffiths","AuId":2122351653},
        #        {"AuN":"mark steyvers","AuId":499903789}],
        #  "F":[{"FN":"dynamic topic model","FId":181389423},
        #       {"FN":"topic model","FId":171686336},
        #	   {"FN":"documentation","FId":56666940},
        #	   {"FN":"latent dirichlet allocation","FId":500882744},
        #	   {"FN":"publishing","FId":151719136},
        #	   {"FN":"probability","FId":104396909},
        #	   {"FN":"monte carlo method","FId":19499675}
        #  ]}]
        #}
        #    public String entryId;
        res.entryId = entity["Id"]

        res.entryTitle = entity["Ti"]

        # public String entryURL;
        res.entryURL = "https://academic.microsoft.com/#/detail/" + str(res.entryId)

        res.entryAbstract = ""
        if entity.has_key("E"):
            ex = json.loads(entity["E"])
            if ex.has_key("IA"):
                regex = re.compile(r"\\n|\\r", re.IGNORECASE)
                IA = ex["IA"]
                IndexLength =IA["IndexLength"]
                InvertedIndex = IA["InvertedIndex"]
                W = ["" for i in xrange(0,IndexLength)]
                for word in InvertedIndex.keys():
                    for pos in InvertedIndex[word]:
                        W[pos] = word
                res.entryAbstract = regex.sub(" "," ".join(W))

        if entity.has_key("Y"):
            res.entryPublished = entity["Y"]
        else:
            res.entryPublished = ""

        if entity.has_key("ECC"):
            res.ECC = int(entity["ECC"])
        else:
            res.ECC = 0

        res.authors = []
        if entity.has_key("AA"):
            for author in entity['AA']:
                a = Author()
                a.id = author["AuId"]
                a.name = author["AuN"]

                if author.has_key("AfN"):
                    a.affiliation = author["AfN"]
                else:
                    a.affiliation = ""

                if author.has_key("AfId"):
                    a.affiliationId = author["AfId"]
                else:
                    a.affiliationId = ""

                res.authors.append(a)


        res.topics = []
        if entity.has_key("F"):
            for topic in entity["F"]:
                t = Topic()
                t.topicId = topic["FId"]
                t.topicName = topic["FN"]
                res.topics.append(t)


        res.referencesTo = []
        if entity.has_key("RId"):
            for topic in entity["RId"]:
                res.referencesTo.append(topic)

        return res
    '''



    '''
    def saveList(self, file, ids):
        thefile = open(file, 'w')
        thefile.write("\n".join([str(i) for i in ids]))
        thefile.close();
    '''



    '''
    def saveEntries(self, file, entries):
        thefile = open(file, 'w')
        for entry in entries:
            thefile.write(entry.toCsv())
            thefile.write("\n")
        thefile.close();
'''




'''
def downloadLevel(dataDir, subscriptionKey, level, files):

    #outQueueFile = dataDir + "/ms-academic-queue-" + str(level) + ".csv"
    #outNextQueueFile  = dataDir + "/ms-academic-queue-" + str(level + 1) + ".csv"
    #outEntriesFile = dataDir + "/ms-academic-entries-" + str(level) + ".csv"
    #outInvalidFile = dataDir + "/ms-academic-invalid.csv"
    #inExcludeTopicsFile = dataDir + "/in-academic-exclude-topics.txt"
    #inIncludeTopicsFile = dataDir + "/in-academic-include-topics.txt"
    #outQueueSizeFile = dataDir + "/ms-academic-queue-size.txt"

    outQueueFile = files['outQueueFile'].format(str(level))
    outNextQueueFile  = files['outQueueFile'].format( str(level + 1) )
    outEntriesFile = files['outEntriesFile'].format( str(level) )
    outInvalidFile = files['outInvalidFile']
    inExcludeTopicsFile = files['inExcludeTopicsFile']
    inIncludeTopicsFile = files['inIncludeTopicsFile']
    outQueueSizeFile = files['outQueueSizeFile']

    api = Api(subscriptionKey)

    # load queue in memory
    msAcademicQueue = api.loadList(outQueueFile);
    msAcademicQueueIds = set(msAcademicQueue);

    # load list of indexed entries in memory
    try:
        msAcademicEntries = api.loadEntries(outEntriesFile);
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print e
        msAcademicEntries = []

    # load ids of indexed entries in memory
    msAcademicIndexedIds = set([])
    for entry in msAcademicEntries:
        msAcademicIndexedIds.add(entry.entryId)

    # load list of invalid entries in memory
    msAcademicInvalidIds = set(api.loadList(outInvalidFile));

    # load set of invalid topics in memory
    msAcademicExcludeTopicsIds = set(api.loadList(inExcludeTopicsFile));


    msAcademicIncludeTopicsIds = api.loadList(inIncludeTopicsFile)


    counter = 1;
    msAcademicQueueUpdate = set();
    ids = []
    requestCounter = 0

    # print msAcademicQueue

    for id in msAcademicQueue:

        # get list of 80 ids from queue
        ids.append(id);

        if counter % 80 == 0 or len(msAcademicQueue) == counter:

            # load by publication ids
            refs = api.loadByIds(ids, msAcademicIncludeTopicsIds)
            requestCounter = requestCounter + 1

            allIds = set();
            for tid in ids:
                allIds.add(tid)

            # print allIds

            for en in refs:
                topicIsValid = True
                for t in en.topics:
                    if  t.topicId in msAcademicExcludeTopicsIds:
                        topicIsValid = false;

                contentIsValid = True
                #TODO: test here if text content is similar to set of the seed publications

                if topicIsValid and contentIsValid:
                    en.level = level
                    msAcademicEntries.append(en)
                    msAcademicIndexedIds.add(en.entryId)
                    if en.entryId in allIds:
                        allIds.remove(en.entryId)

                    for newId in en.referencesTo:
                        if (newId not in msAcademicIndexedIds) and (newId not in msAcademicInvalidIds) and (newId not in msAcademicQueueIds):
                            msAcademicQueueUpdate.add(newId)


                print str(counter) + " of " + str(len(msAcademicQueue)) + " : " + str(en.entryId) + "  " + str(en.entryPublished) + "  ", en.entryTitle.encode('utf-8')

            for tid in allIds:
                msAcademicInvalidIds.add(tid);

            # load by publication rids
            referencedBy = api.loadByRIds(ids, msAcademicIncludeTopicsIds)
            requestCounter = requestCounter + 1
            for entry in referencedBy:
                newId = entry.entryId
                if (newId not in msAcademicIndexedIds) and (newId not in msAcademicInvalidIds) and (newId not in msAcademicQueueIds):
                    msAcademicQueueUpdate.add(newId)


            # save queue size
            queueSize = len(msAcademicQueueUpdate) + len(msAcademicQueue) - counter
            print "NewQueueSize = " + str(queueSize)

            thefile = open(outQueueSizeFile, 'a')
            thefile.write("\n" + str(queueSize))
            thefile.close();

            print counter, " of ", len(msAcademicQueue), " - OK"
            print "requestCounter = " + str(requestCounter)

            ids = []

        counter = counter + 1


    # save results
    api.saveList(outInvalidFile, msAcademicInvalidIds)

    api.saveEntries(outEntriesFile, msAcademicEntries);

    api.saveList(outNextQueueFile, msAcademicQueueUpdate);

    print msAcademicQueueUpdate


'''



'''
