import numpy as np
from time import time
import sklearn_crfsuite
import sklearn_crfsuite.metrics

file_names = ["kompas.txt","detik.txt","tempo.txt","beritasatu.txt","metro.txt"]
tweet_list = []
pos_tags = []
name_entities = []
tags = []
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
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(x_train,y_train)
labels = list(crf.classes_)
print(labels)

print("Input")
#Data Test
y_pred = crf.predict(x_train)
print(sklearn_crfsuite.metrics.flat_f1_score(y_train, y_pred, average='weighted', labels=labels))

#Construct list of (list of key word)
i = 0
for pred in y_pred:
    sentence = tweet_list[i].strip().split(' ')
    j = 0
    tmp = []
    for label in pred: 
        if (label == '1'):
            tmp.append(sentence[j])
        j+=1
    if (tmp != []):
        key_words.append(tmp)
    i+=1