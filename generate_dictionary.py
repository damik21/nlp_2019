from collections import OrderedDict


resultFile = open("/Users/kapmayn/Downloads/dictionaries/dictionary_3.txt", 'w')
line = open("/Users/kapmayn/Downloads/processed/processed_3.txt", 'r').read()

words = line.lower().split()
resultSet = OrderedDict()

for word in words:
    if resultSet.get(word):
        resultSet[word] += 1
    else:
        resultSet.update({word: 1})

sortedX = sorted(resultSet.items(), key=lambda kv: kv[1], reverse=True)
sortedDict = OrderedDict(sortedX)

for key, value in sortedDict.items():
    resultFile.write(key + ":" + str(value) + "\n")
