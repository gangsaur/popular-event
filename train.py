from pystruct.models import GraphCRF
from pystruct.learners import NSlackSSVM
from time import time
import numpy as np
from sklearn.datasets import load_iris
import sklearn_crfsuite
import sklearn_crfsuite.metrics
from pystruct.models import GraphCRF
from pystruct.learners import NSlackSSVM

file_name = "detik.txt"
f = open (file_name, 'r')
i = 0

tweet_list = []
pos_tags = []
name_entities = []
tags = []

for line in f:
    i += 1
    if (i % 5 == 1):
        tweet_list.append(line)
    if (i % 5 == 2):
        pos_tags.append(line.split(' '))
    if (i % 5 == 3):
        name_entities.append(line.split(' '))
    if (i % 5 == 0):
        tags.append(line.split(' '))

i = 0
x_train = []
y_train = []

for sentence in tweet_list:
    word_tokens = sentence.strip().split(' ')
    j = 0
    x_train_sentence = []
    y_train_sentence = []
    for token in word_tokens:
        x_train_sentence.append({token,pos_tags[i][j],name_entities[i][j]})
        y_train_sentence.append(tags[i][j])
        j+=1
    i+=1
    x_train.append(x_train_sentence)
    y_train.append(y_train_sentence)

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


#Data Test
# y_pred = crf.predict(x_train)
#
# print(sklearn_crfsuite.metrics.flat_f1_score(y_train, y_pred,
#                       average='weighted', labels=labels))
