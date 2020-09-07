from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer() 


def LematizationWord(content):
   con  = [] 
   for w in content:
      con.append(lemmatizer.lemmatize(w))
   return con
