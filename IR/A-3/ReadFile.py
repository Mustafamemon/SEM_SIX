import os
import re
import math
import json
from collections import Counter

from LematizationWord import LematizationWord
from StemmingWord import StemmingWord


def ReadTrainFile(percent):
    folder_path = os.path.abspath('bbcsport')
    stop_word_path = os.path.abspath("Stopword-List.txt")
    
    file           = open(stop_word_path, "r")
    stop_word      = file.read()
    stop_word      = stop_word.split('\n')
    stop_word      = [i for i in stop_word if i]
    special_char   = ['.',' ',',','[',']','(',')','"',':','?','','-','\n','/b','\j','"']
    
    content        = ""
    doc_frq        = {}
    all_doc        = {}
    
    for nested_folder_path, subdirs, files in os.walk(folder_path):
        if len(subdirs) is 0:
            all_vocab      = []
            _class = os.path.basename(nested_folder_path)

            del files[len(files)-percent:len(files)]
            for file_path in files:
                file     = open(nested_folder_path +'\\'+ file_path , "r")
                content  =  file.read()

                content_list   =  re.split(r'(\.|,|"|/b|\[|\]|—| |:|\(|\)|"|\?|\n|-)+',content)
                content_list  =  [x.lower() for x in content_list]

                r_special_char =  list(set(content_list)-set(special_char))
        
                r_stop_word    =  list(set(r_special_char) - set(stop_word))

                stem_vocab     = StemmingWord(r_stop_word)
        
                doc_count      = {}
                doc_count      = doc_count.fromkeys(stem_vocab,1)
                
                doc_frq        = Counter(doc_frq) + Counter(doc_count)
                
                all_vocab.append(stem_vocab)
            
            all_doc[_class] = all_vocab
            
                
                
    filter_doc_frq  = {}
    for (k,v) in doc_frq.items():
        if v >= 3:
            filter_doc_frq[k] = v
    
    return (all_doc,filter_doc_frq)


def VSM(all_doc ,doc_frq ,total_doc):
    vsm       = {} 
    vocab     = doc_frq.keys()
    for doc in all_doc:
        all_doc_vector = []
        for i in range(0,len(all_doc[doc])):
            doc_vector = []
            for word in vocab:
                tf  = all_doc[doc][i].count(word)
                idf = math.log10(total_doc/ doc_frq[word])
                doc_vector.append(tf*idf)
            all_doc_vector.append(doc_vector)
        vsm[doc] = all_doc_vector
    # file_path = os.path.abspath("")
    
    return vsm
    # save_file = {
    #     'vsm'       :  vsm,
    #     'doc_frq'   :  doc_frq,
    #     'vocab'     :  vocab,
    #     'classes'   : classes
    # }
    # dict = json.dumps(save_file)
    # print(type(save_file))
    # # file = open(file_path+'\index.json','w')
    # file.write(save_file)
    # file.close()


def ReadTestFile(percent):
    folder_path = os.path.abspath('bbcsport')
    stop_word_path = os.path.abspath("Stopword-List.txt")
    
    file           = open(stop_word_path, "r")
    stop_word      = file.read()
    stop_word      = stop_word.split('\n')
    stop_word      = [i for i in stop_word if i]
    special_char   = ['.',' ',',','[',']','(',')','"',':','?','','-','\n','/b','\j','"']
    
    content        = ""
    all_doc        = {}
    
    for nested_folder_path, subdirs, files in os.walk(folder_path):
        if len(subdirs) is 0:
            all_vocab      = []
            _class = os.path.basename(nested_folder_path)
            del files[:len(files)-percent]
            for file_path in files:
                file           =  open(nested_folder_path +'\\'+ file_path , "r")
                content        =  file.read()

                content_list   =  re.split(r'(\.|,|"|/b|\[|\]|—| |:|\(|\)|"|\?|\n|-)+',content)
                content_list   =  [x.lower() for x in content_list]

                r_special_char =  list(set(content_list)-set(special_char))
        
                r_stop_word    =  list(set(r_special_char) - set(stop_word))

                stem_vocab     = StemmingWord(r_stop_word)
        
                all_vocab.append(stem_vocab)
            all_doc[_class] = all_vocab
    
    return all_doc




def CosineSimilarity(x,y):
    x_dot_y = sum(_x * _y for _x,_y in zip(x, y))
    mag_x = math.sqrt(sum(x_i*x_i for x_i in x))
    mag_y = math.sqrt(sum(y_i*y_i for y_i in y))

    return x_dot_y / (mag_x*mag_y)

def EuclideanDistance():
    pass
        

def ApplyKNN(test_vsm,train_vsm,k):
    acc = 0
    for test_doc in test_vsm:
        
        for x in test_vsm[test_doc]:
            sim_all_doc = []
            for train_doc in train_vsm:
                for i in range(0,len(train_vsm[train_doc])):
                    y   = train_vsm[train_doc][i]
                    sim = CosineSimilarity(x,y)
                    sim_all_doc.append((sim,i,train_doc))
            sim_all_doc.sort(reverse=True)
            # print({test_doc:sim_all_doc})
            # print(sim_all_doc[0][2],test_doc)
            if sim_all_doc[0][2] == test_doc:
                acc = acc + 1
    
    return acc
            
            
if __name__ == '__main__':
    # for test data 
    train_doc ,doc_frq  = ReadTrainFile(30)
    
    total_doc = sum([len(doc) for doc in train_doc.values()])
    
    print('done train reading ...')
    
    train_vsm = VSM(train_doc ,doc_frq ,total_doc)
    
    print('done VSM')
    
    print('done train VSM')
    
    # for test data
    
    test_doc  = ReadTestFile(30)

    print('done test reading')
    
    test_vsm = VSM(test_doc ,doc_frq ,total_doc)
    
    print('done test VSM')
    
    total_doc = sum([len(doc) for doc in test_doc.values()])
    
    res = ApplyKNN(test_vsm,train_vsm,3)
    print(res)

    print('ACC : ',res/total_doc)
    
    