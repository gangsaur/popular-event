import numpy as np
import Levenshtein
from time import time
import sklearn_crfsuite
import sklearn_crfsuite.metrics
import os

file_names = ["kompas.txt","detik.txt","tempo.txt","beritasatu.txt","metro.txt"]
tweet_list = []
pos_tags = []
name_entities = []
tags = []
in_tweet_list = []
in_pos_tags = []
in_name_entities = []
in_tags = []
key_words = []

#Read All Files
for file_name in file_names:
    #Open
    f = open ("./data/" + file_name, 'r', encoding="UTF-8")
    i = 0

    #Append to array
    for line in f:
        i += 1
        if (i % 5 == 1):
            tweet_list.append(line)
        if (i % 5 == 2):
            pos_tags.append(line.strip().split(' '))
        if (i % 5 == 3):
            name_entities.append(line.strip().split(' '))
        if (i % 5 == 0):
            tags.append(line.strip().split(' '))

    #Close
    f.close()
        
i = 0
x_train = []
y_train = []
x_test = []
y_test = []

#Make into features
for sentence in tweet_list:
    word_tokens = sentence.strip().split(' ')
    j = 0
    x_train_sentence = []
    y_train_sentence = []
    for token in word_tokens:
        x_train_sentence.append([token,pos_tags[i][j],name_entities[i][j]])
        y_train_sentence.append(tags[i][j])
        j+=1
    i+=1
    x_train.append(x_train_sentence)
    y_train.append(y_train_sentence)

#Init Classifier and Train
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.01,
    c2=0.01,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(x_train,y_train)
labels = list(crf.classes_)
print(labels)

print("Choose Test Data")
print("1. Test with Train")
print("2. Read from ./data/input.txt")
mode = input("(1/2)")
if (mode == "1"):
    #Data Test
    y_pred = crf.predict(x_train)
    print("F1 Score : " + str(sklearn_crfsuite.metrics.flat_f1_score(y_train, y_pred, average='weighted', labels=labels)))
else:
    print("With Label?")
    labelArgs = input("(Y/N)")
    os.system("java -jar indonesia-ner.jar " + labelArgs)
    f = open ("./data/process/output.txt", 'r', encoding="UTF-8")
    i = 0

    #Append to array
    for line in f:
        i += 1
        if (i % 5 == 1):
            in_tweet_list.append(line)
        if (i % 5 == 2):
            in_pos_tags.append(line.strip().split(' '))
        if (i % 5 == 3):
            in_name_entities.append(line.strip().split(' '))
        if (i % 5 == 0):
            in_tags.append(line.strip().split(' '))    
    
    f.close()
    
    i = 0
    #Make into features
    for sentence in in_tweet_list:
        word_tokens = sentence.strip().split(' ')
        j = 0
        x_test_sentence = []
        y_test_sentence = []
        for token in word_tokens:
            x_test_sentence.append([token,in_pos_tags[i][j],in_name_entities[i][j]])
            y_test_sentence.append(in_tags[i][j])
            j+=1
        i+=1
        x_test.append(x_test_sentence)
        y_test.append(y_test_sentence)
        
    #Data Test
    y_pred = crf.predict(x_test)

#Construct list of (list of key word)
i = 0
for pred in y_pred:
    if (mode == "1"):
        sentence = tweet_list[i].strip().split(' ')
    else:
        sentence = in_tweet_list[i].strip().split(' ')        
    j = 0
    tmp = str()
    for label in pred: 
        if (label == '1'):
            tmp += sentence[j] + ' '
        j+=1
    if (tmp != ''):
        key_words.append(tmp.rstrip())
    i+=1

labeled = []
score = {}
treshold = 0.5

for i in range(len(key_words)):
    if i not in labeled:
        for j in range(i + 1, len(key_words)):
            if j not in labeled:
                if Levenshtein.ratio(key_words[i], key_words[j]) > treshold:
                    labeled.append(j)
                    if i in score.keys():
                        score[i] += 1
                    else:
                        score[i] = 1

sorted_score = [(k, score[k]) for k in sorted(score, key=score.get, reverse=True)]
rank = 1
for key, value in sorted_score:
    print (str(rank) + '. ' + key_words[key])
    rank += 1
    if rank > 10:
        break
