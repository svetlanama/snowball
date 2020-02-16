# import PyPDF2
from os import listdir
from os.path import isfile
from os.path import join
import pandas as pd
import random
import time


def compose_datasets(txt_file_dir, dataset_file_dir, increment_size=1, increment_strategy='time-asc', citations=False):
    # print txt_files
    # compose file lists
    strategy_found=False
    if increment_strategy == 'time-asc':
        t0 = time.time()
        strategy_found=True
        # read txt files
        txt_files = sorted([join(txt_file_dir, f) for f in listdir(txt_file_dir) if isfile(join(txt_file_dir, f)) and f.lower().endswith(".txt")])
        cnt = 0
        n_dataset = 0
        dataset = ''
        fnames=[]
        for i in range(0, len(txt_files)):
            fl = open(txt_files[i], 'r')
            dataset += fl.read()
            fnames.append(txt_files[i])
            fl.close()
            cnt += 1
            if cnt % increment_size == 0:
                n_dataset += 1
                fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
                fl = open(fnm, 'w')
                fl.write(dataset)
                fl.close()
                t1 = time.time()
                print n_dataset, fnm, t1 - t0,'sec',fnames
                print "\n"
                
        if cnt % increment_size > 0:
            n_dataset += 1
            fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
            fl = open(fnm, 'w')
            fl.write(dataset)
            fl.close()
            t1 = time.time()
            print n_dataset, fnm, t1 - t0,'sec',fnames
            print "\n"

    if increment_strategy == 'time-desc':
        t0 = time.time()
        strategy_found=True
        # read txt files
        txt_files = sorted([join(txt_file_dir, f) for f in listdir(txt_file_dir) if isfile(join(txt_file_dir, f)) and f.lower().endswith(".txt")])
        txt_files = txt_files[::-1]
        cnt = 0
        n_dataset = 0
        dataset = ''
        fnames=[]
        for i in range(0, len(txt_files)):
            fl = open(txt_files[i], 'r')
            dataset += fl.read()
            fnames.append(txt_files[i])
            fl.close()
            cnt += 1
            if cnt % increment_size == 0:
                n_dataset += 1
                fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
                fl = open(fnm, 'w')
                fl.write(dataset)
                fl.close()
                t1 = time.time()
                print n_dataset, fnm, t1 - t0,'sec',fnames
                print "\n"

        if cnt % increment_size > 0:
            n_dataset += 1
            fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
            fl = open(fnm, 'w')
            fl.write(dataset)
            fl.close()
            t1 = time.time()
            print n_dataset, fnm, t1 - t0,'sec',fnames
            print "\n"

    if increment_strategy == 'random':
        t0 = time.time()
        strategy_found=True
        # read txt files
        txt_files = sorted([join(txt_file_dir, f) for f in listdir(txt_file_dir) if isfile(join(txt_file_dir, f)) and f.lower().endswith(".txt")])
        random.shuffle(txt_files)
        cnt = 0
        n_dataset = 0
        dataset = ''
        fnames=[]
        for i in range(0, len(txt_files)):
            fl = open(txt_files[i], 'r')
            dataset += fl.read()
            fnames.append(txt_files[i])
            fl.close()
            cnt += 1
            if cnt % increment_size == 0:
                n_dataset += 1
                fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
                fl = open(fnm, 'w')
                fl.write(dataset)
                fl.close()
                t1 = time.time()
                print n_dataset, fnm, t1 - t0,'sec',fnames
                print "\n"

        if cnt % increment_size > 0:
            n_dataset += 1
            fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
            fl = open(fnm, 'w')
            fl.write(dataset)
            fl.close()
            t1 = time.time()
            print n_dataset, fnm, t1 - t0,'sec',fnames
            print "\n"

    if increment_strategy == 'time-bidir':
        t0 = time.time()
        strategy_found=True
        # read txt files
        txt_files = sorted([join(txt_file_dir, f) for f in listdir(txt_file_dir) if isfile(join(txt_file_dir, f)) and f.lower().endswith(".txt")])
        cnt = 0
        n_dataset = 0
        dataset = ''
        fnames=[]
        n_files = len(txt_files)
        i_max = int(len(txt_files) / 2)
        for i1 in range(0, i_max):

            fl = open(txt_files[i1], 'r')
            dataset += fl.read()
            fnames.append(txt_files[i1])
            fl.close()

            i2 = n_files-i1-1
            fl = open(txt_files[i2], 'r')
            dataset += fl.read()
            fnames.append(txt_files[i2])
            fl.close()

            cnt += 2
            if cnt % increment_size == 0:
                n_dataset += 1
                fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
                fl = open(fnm, 'w')
                fl.write(dataset)
                fl.close()
                t1 = time.time()
                print n_dataset, fnm, t1 - t0,'sec',fnames
                print "\n"

        if cnt % increment_size > 0:
            n_dataset += 1
            fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
            fl = open(fnm, 'w')
            fl.write(dataset)
            fl.close()
            t1 = time.time()
            print n_dataset, fnm, t1 - t0,'sec',fnames
            print "\n"


    if increment_strategy == 'citation-desc':
        t0 = time.time()
        strategy_found=True
        # read citations file
        df1=pd.read_excel(citations).fillna(value=0)
        df1=df1[["No Citations","paper file name"]]

        # read txt files
        txt_files = [f for f in listdir(txt_file_dir) if isfile(join(txt_file_dir, f)) and f.lower().endswith(".txt")]
        df2=pd.DataFrame(data=txt_files, columns=["paper file name"])
        df2['paths']=[join(txt_file_dir, f) for f in txt_files]

        # sort by citations
        df=pd.merge(df2, df1, how='left', on="paper file name").sort_values(by=["No Citations"], ascending=False)
        # print(df)
        sorted_txt_files=list(df['paths'])
        # print(sorted_txt_files)
     
        cnt = 0
        n_dataset = 0
        dataset = ''
        fnames=[]
        for i in range(0, len(sorted_txt_files)):
            fl = open(sorted_txt_files[i], 'r')
            dataset += fl.read()
            fnames.append(sorted_txt_files[i])
            fl.close()
            cnt += 1
            if cnt % increment_size == 0:
                n_dataset += 1
                fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
                fl = open(fnm, 'w')
                fl.write(dataset)
                fl.close()
                t1 = time.time()
                print n_dataset, fnm, t1 - t0,'sec',fnames
                print "\n"

        if cnt % increment_size > 0:
            n_dataset += 1
            fnm = join(dataset_file_dir, 'D' + (('0000000000000000000000000000000000' + str(n_dataset))[-10:]) + '.txt')
            fl = open(fnm, 'w')
            fl.write(dataset)
            fl.close()
            t1 = time.time()
            print n_dataset, fnm, t1 - t0,'sec',fnames
            print "\n"

    if not  strategy_found:
        print("strategy not found")
    return strategy_found








