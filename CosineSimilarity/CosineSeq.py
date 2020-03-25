
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import glob, os
import re
import csv

ps = PorterStemmer()
sw = stopwords.words('english')
lem = WordNetLemmatizer()

fileAddress1Final = []
fileAddress2Final = []
CosineFinal = []

Speechpath = "/home/hoomanvhd/Desktop/DATASET/Video2-done/VideoTextReadByLineSilent/*.txt"

SpeechTextList1 = []
SpeechTextList2 = []


for SpeechTextFile in sorted(glob.glob(Speechpath)):
    SpeechEXT = os.path.splitext(SpeechTextFile)
    SpeechTextList1.append(SpeechTextFile)

SpeechTextList2 = SpeechTextList1.copy()

ps = PorterStemmer()
sw = stopwords.words('english')
lem = WordNetLemmatizer()

for Speech1 in SpeechTextList1:
    with open(Speech1, "r") as SpeechFile1:
        reader1 = SpeechFile1.read()

    X = reader1
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

    for Speech2 in SpeechTextList2:
        with open(Speech2, "r") as SpeechFile2:
            reader2 = SpeechFile2.read()

        Y = reader2
        Y = Y.lower()
        Y_token = word_tokenize(Y)
        Y_list = []

        for words in Y_token:
            words = ps.stem(words)
            wordslem = lem.lemmatize(words)
            Y_list.append(words)
            if words != wordslem:
                Y_list.append(wordslem)

        Y_set = [wordY for wordY in Y_list if not wordY in sw]

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
            c += l1[i] * l2[i]

        cosine = (c / float((sum(l1) * sum(l2)) ** 0.5))
        CosineFinal.append(cosine)

        fileAddress1 = str(SpeechFile1)
        fileAddress1Clear = re.findall("VideoTextReadByLineSilent/(.*?)'", fileAddress1)
        fileAddress1Clear = str(fileAddress1Clear)
        fileAddress1Clear = fileAddress1Clear.replace("'", "")
        fileAddress1Clear = fileAddress1Clear.replace("[", "")
        fileAddress1Clear = fileAddress1Clear.replace("]", "")
        fileAddress1Final.append(fileAddress1Clear)

        fileAddress2 = str(SpeechFile2)
        fileAddress2Clear = re.findall("VideoTextReadByLineSilent/(.*?)'", fileAddress2)
        fileAddress2Clear = str(fileAddress2Clear)
        fileAddress2Clear = fileAddress2Clear.replace("'", "")
        fileAddress2Clear = fileAddress2Clear.replace("[", "")
        fileAddress2Clear = fileAddress2Clear.replace("]", "")
        fileAddress2Final.append(fileAddress2Clear)

with open("/home/hoomanvhd/Desktop/DATASET/Video2-done/CosineResultOFsegments.csv", "w") as writingFile:
    writer = csv.writer(writingFile)
    writer.writerows(zip(fileAddress1Final, fileAddress2Final, CosineFinal))



