import re
import json
import os
import math
import copy
from collections import Counter
import lematization as l

file_path = os.path.abspath("")


def readFile():
    f=open(file_path+'\Stopword-List.txt', "r")
    stop_word    = f.read()
    stop_word    = stop_word.split('\n')
    stop_word    = [i for i in stop_word if i]
    content      = ""
    special_char = ['.',' ',',','[',']','(',')','"',':','?','','-']
    VSM          = []
    vocab        = []
    doc_frq      = {}
    for doc_no in range(0,56):
        f              =  open(file_path+'\Trump Speechs\speech_'+str(doc_no)+'.txt', "r")
        content        =  f.read()
        content        =  content.split('\n')[1]

        content_list   =  re.split(r'(\.|,|\[|\]|—| |:|\(|\)|"|\?|\\n|-)+',content)

        content_list    =  [x.lower() for x in content_list]
        
        r_special_char =  list(set(content_list)-set(special_char))
        
        r_stop_word    =  list(set(r_special_char) - set(stop_word))
        
        lema_vocab     =  l.lematization_word(r_stop_word)
        
        vocab          =  vocab + lema_vocab
        vocab          =  list(set(vocab))
        term_count     = {}
        
        temp           = {}
        temp           = temp.fromkeys(lema_vocab,1)
        doc_frq        = Counter(doc_frq) + Counter(temp)
        
        
        for j in range(0,len(lema_vocab)):
            if lema_vocab[j] in term_count:
                term_count[lema_vocab[j]] = term_count[lema_vocab[j]] + content_list.count(r_stop_word[j])
            else:
                term_count[lema_vocab[j]] = content_list.count(r_stop_word[j])
        
        VSM.append(term_count)
        
        print("processing ...",doc_no)
    
    for doc_no in range(0,56):
        for word in vocab:
            
            if word in VSM[doc_no]:
                VSM[doc_no][word] = VSM[doc_no][word]*math.log10(56 / doc_frq[word])   
    save_file = {
        'VSM'       :  VSM,
        'doc_frq'   :  doc_frq,
        'vocab'     :  vocab,
        'stop_word' :  stop_word,
    }
    f = open(file_path+'\index.json','w')
    dict = json.dumps(save_file)
    f.write(dict)
    f.close()


