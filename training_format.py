import sys
import os

def reformat(fname, finputname, foutputname):
    with open(fname) as f, \
        open(finputname, 'w') as finput, \
        open(foutputname, 'w') as foutput:
        for line in f:
            lines = line.strip().split('\t')
            # print(lines)
            lemma = lines[0].replace(' ', '+')
            morp = lines[1].replace(' ', '+')
            # lemma = lines[0]
            # morp = lines[1]
            msd = lines[-1]
            if len(lines) == 3:
                form = lines[1]
            if len(lines) == 2:
                form = '-'
            output = [letter for letter in morp] 
            input = [letter for letter in lemma]
            out_new = ' '.join(output) + '\n'
            in_new = ' '.join(input) + '\n'
            finput.write(in_new)
            foutput.write(out_new.replace(' + @ @ ',' @@ '))

if __name__ == '__main__':
    lang = 'git'  # language code of 3 letters for Sigmorphon 2020 shared task0


    train = 'data_4fairseq_train_git.txt' 
    trainin = 'train.' + lang + '.input'
    trainout = 'train.' + lang + '.output'

    if os.path.exists(train):
        reformat(train, trainin, trainout)

    dev = 'data_4fairseq_dev_git.txt'
    devin = 'dev.' + lang + '.input'
    devout = 'dev.' + lang + '.output'
    if os.path.exists(dev):
        reformat(dev, devin, devout)

    test = 'data_4fairseq_test_git.txt'
    testin = 'test.' + lang + '.input'
    testout = 'test.' + lang + '.output'
    if os.path.exists(test):
        reformat(test, testin, testout)
