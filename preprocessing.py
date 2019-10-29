import os
import io 
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import pubmed_parser as pp

nltk.download('stopwords')

punctuations = '+,.<=>!?()[]{}'

stop_words = set(stopwords.words('english'))
resultFile = open("/Users/kapmayn/Downloads/processed/processed.txt", 'w')
line = open("/Users/kapmayn/Downloads/pubmed_oa/abstracts.txt", 'r').read()
words = line.split()
for word in words:
	lowerWord = word.lower().translate(str.maketrans('', '', punctuations))
	if not lowerWord in stop_words:
		resultFile.write(lowerWord + " ")