
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import glob, os
import re
import csv

Querypath = "/home/hoomanvhd/Desktop/DATASET/Video2-done/to-search/*.txt"

QueryTextList = []

for QueryTextFile in sorted(glob.glob(Querypath)):
    QueryEXT = os.path.splitext(QueryTextFile)
    QueryTextList.append(QueryTextFile)

QueryText = []
QueryAddress = []
for Query in QueryTextList:
    with open(Query, "r") as Queryfile:
        reader = Queryfile.read()
    QueryText.append(reader)
    QueryAddress.append(Queryfile)

Speechpath = "/home/hoomanvhd/Desktop/DATASET/Video2-done/VideoTextReadByLineSilent/*.txt"

SpeechTextList = []


for SpeechTextFile in sorted(glob.glob(Speechpath)):
    SpeechEXT = os.path.splitext(SpeechTextFile)
    SpeechTextList.append(SpeechTextFile)


ps = PorterStemmer()
sw = stopwords.words('english')
lem = WordNetLemmatizer()


cosineFinal = []
XFinal = []
YFinal = []
fileAddressFinal = []
QueryAddressFinal = []

for elementX in range(len(QueryText)):
    QAddress = QueryAddress[elementX]
    X = QueryText[elementX]
    X = X.lower()
    X_token = word_tokenize(X)
    X_list = []

    for words in X_token:
        words = ps.stem(words)
        wordslem = lem.lemmatize(words)
        X_list.append(words)
        if words != wordslem:
            X_list.append(wordslem)

    X_set = {wordX for wordX in X_list if not wordX in sw}


    for Speech in SpeechTextList:
        with open(Speech, "r") as Speechfile:

            reader = Speechfile.read()

        Y = reader
        Y = Y.lower()
        Y_token = word_tokenize(Y)
        Y_list = []

        for words in Y_token:
            words = ps.stem(words)
            wordslem = lem.lemmatize(words)
            Y_list.append(words)
            if words != wordslem:
                Y_list.append(wordslem)

        Y_set = {wordY for wordY in Y_list if not wordY in sw}

        rvector = X_set.union(Y_set)

        l1 = []
        l2 = []

        for w in rvector:
            if w in X_set:
                 l1.append(1)
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)

        c = 0

        for i in range(len(rvector)):
            c += l1[i]*l2[i]

        cosine = (c / float((sum(l1)*sum(l2))**0.5))
        cosineFinal.append(cosine)
        fileAddress1 = str(Speechfile)
        fileAddressClear = re.findall("VideoTextReadByLineSilent/(.*?)'", fileAddress1)
        fileAddress = str(fileAddressClear)
        fileAddress = fileAddress.replace("'", "")
        fileAddress = fileAddress.replace("[", "")
        fileAddress = fileAddress.replace("]", "")
        fileAddressFinal.append(fileAddress)

        XFinal.append(X)
        YFinal.append(Y)

        QAddress1 = str(QAddress)
        QAddress1Clear = re.findall("/to-search/(.*?)' mode='r'", QAddress1)
        QAddressF = str(QAddress1Clear)
        QAddressF = QAddressF.replace("'", "")
        QAddressF = QAddressF.replace("[", "")
        QAddressF = QAddressF.replace("]", "")
        QueryAddressFinal.append(QAddressF)




with open("/home/hoomanvhd/Desktop/DATASET/Video2-done/CosineResultSilent.csv", "w") as writingFile:
        writer = csv.writer(writingFile)
        writer.writerows(zip(QueryAddressFinal, fileAddressFinal, cosineFinal))





















