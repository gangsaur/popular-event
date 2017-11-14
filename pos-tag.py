import nltk

#function to extract feature
def extract_feature(word):
  return {
    'word': word,
    'is_capitalized': word[0].upper() == word[0],
    'is_all_caps': word.upper() == word,
    'is_all_lower': word.lower() == word,
    'prefix-1': word[0],
    'prefix-2': word[:2],
    'prefix-3': word[:3],
    'suffix-1': word[-1],
    'suffix-2': word[-2:],
    'suffix-3': word[-3:],
    'has_hyphen': '-' in word,
    'is_numeric': word.isdigit(),
    'capitals_inside': word[1:].lower() != word[1:] }


#opening UD file and extracting the features from data
f = open('data/id-ud-train.conllu', 'r', encoding="utf8")
data_set = []
# label_list = []
# feature_list = []
for line in f:
  sentence = line.split("\t")
  if sentence[0].isdigit():
    # feature_list.append(extract_feature(sentence[1]) )
    # label_list.append(sentence[3])
    data_set.append(
      ( extract_feature(sentence[1]) , sentence[3])
    )

f.close()
train_set,test_set = data_set[300:],data_set[:300]

print("start train")
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))


