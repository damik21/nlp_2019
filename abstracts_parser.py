import os
import pubmed_parser as pp

nlpPath = "/Users/kapmayn/Desktop/nlp"
articlesFolderPath = nlpPath + "/articles"
abstractsFilePath = nlpPath + "/abstracts.txt"

articlesFileNameList = os.listdir(articlesFolderPath)
articlesFileNameList(reverse = True)
resultFile = open(abstractsFilePath, 'w')

for fileName in articlesFileNameList:
	print(fileName)
	dictOut = pp.parse_medline_xml(articlesFolderPath + "/" + fileName)
	for item in dictOut:
		resultFile.write((item['abstract'] + '\n'))