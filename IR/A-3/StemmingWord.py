from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


ps = PorterStemmer()

def StemmingWord(content):
    con  = []
    for w in content:
       con.append(ps.stem(w))
    return con


