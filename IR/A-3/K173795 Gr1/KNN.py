import os
import re
import json
import math
import numpy 
import random
import statistics

from collections import Counter
from StemmingWord import StemmingWord

def clean(content):
    file_path = os.path.abspath("Stopword-List.txt")
    
    file           = open(file_path, "r")
    stop_word      = file.read()
    stop_word      = stop_word.split('\n')
    stop_word      = [i for i in stop_word if i]
    special_char   = ['.',' ',',','[',']','(',')','"',':','?','','-','\n','/b','\j','"',';']
    
    content_list   =  re.split(r'(\.|,|;|"|/b|\[|\]|—| |:|\(|\)|"|\?|\n|-)+',content)
    content_list   =  [x.lower() for x in content_list]

    r_special_char =  list(set(content_list)-set(special_char))
        
    r_stop_word    =  list(set(r_special_char) - set(stop_word))

                
    return r_stop_word

def ReadFile(percent):
    folder_path = os.path.abspath('bbcsport')
    
    content        = ""
    doc_frq        = {}
    all_train_doc  = {}
    all_test_doc   = {}
    actual_output  = {}
    
    for nested_folder_path, subdirs, files in os.walk(folder_path):
        if len(subdirs) is 0:
            
            all_test_vocab        = []
            all_train_vocab       = []
            _class                = os.path.basename(nested_folder_path)
            
            random.shuffle(files)
            
            train_files = math.ceil(len(files)*percent)
            
            test_files  = len(files) - train_files 
            
            actual_output[_class] = test_files
            
            
            for i in range(0,train_files):
                file_path      = files[i]
                file           = open(nested_folder_path +'\\'+ file_path , "r")
                
                content        =  file.read()
                
                r_stop_word    = clean(content)
                
                stem_vocab     = StemmingWord(r_stop_word)
        
                doc_count      = {}
                doc_count      = doc_count.fromkeys(stem_vocab,1)
                
                doc_frq        = Counter(doc_frq) + Counter(doc_count)
                
                all_train_vocab.append(stem_vocab)
            
            all_train_doc[_class] = all_train_vocab

            for i in range(train_files,train_files+test_files):
                file_path      = files[i]
                file           = open(nested_folder_path +'\\'+ file_path , "r")
                
                content        =  file.read()
                
                r_stop_word    = clean(content)
                
                stem_vocab     = StemmingWord(r_stop_word)
        
                all_test_vocab.append(stem_vocab)
            
            
            all_test_doc[_class] = all_test_vocab
        
    filter_doc_frq  = {}
    for (k,v) in doc_frq.items():
        if v >= 3:
            filter_doc_frq[k] = v
        
    return (all_test_doc,all_train_doc,filter_doc_frq,actual_output)

def VSM(all_doc ,doc_frq ,total_doc):
    vsm       = {} 
    vocab     = doc_frq.keys()
    for doc in all_doc:
        all_doc_vector = []
        for i in range(0,len(all_doc[doc])):
            doc_vector = []
            doc_vector = [all_doc[doc][i].count(word)*math.log10(total_doc/ doc_frq[word]) for word in vocab]
            all_doc_vector.append(doc_vector)
        vsm[doc] = all_doc_vector
    
    return vsm
    

def CosineSimilarity(x,y):
    x_dot_y = numpy.dot(x,y)
    mag_x   = numpy.linalg.norm(x)
    mag_y   = numpy.linalg.norm(y)
    
    return x_dot_y / (mag_x*mag_y)

# def EuclideanDistance(x,y):
#     x = numpy.array(x)
#     y = numpy.array(y)
#     return numpy.linalg.norm(x - y).item()
        

def ApplyKNN(test_vsm,train_vsm,k):
    classes        = test_vsm.keys()
    predict_output = { i:0  for i in classes} 
    for test_doc in test_vsm:
        for x in test_vsm[test_doc]:
            sim_all_doc = [(0,0,None) for k in range(0,k)]
            for train_doc in train_vsm:
                for i in range(0,len(train_vsm[train_doc])):
                    y   = train_vsm[train_doc][i]
                    sim = CosineSimilarity(x,y)
                    if min(sim_all_doc)[0] <= sim:
                        sim_all_doc[sim_all_doc.index(min(sim_all_doc))] = (sim,i,train_doc)
            
            k_classes = [c for s,i,c in sim_all_doc]
            try:
                prd_class = statistics.mode(k_classes)
            except statistics.StatisticsError:
                prd_class = k_classes[0]
            
            if prd_class == test_doc:
                predict_output[test_doc] = predict_output[test_doc] + 1 
            
    return  predict_output
def AccuracyEachLabel(predict_output,actual_output):
    accuracy = {}
    for c in actual_output:
        try:
           accuracy[c]  = (predict_output[c] / actual_output[c]) * 100
        except KeyError:
            accuracy[c] = 0
    return accuracy



    

if __name__ == "__main__":
    ratio = 70 / 100 
    K     = 3
    test_doc , train_doc, doc_frq , actual_output  = ReadFile(ratio)
    
    total_train_doc = sum([len(doc) for doc in train_doc.values()])
    total_test_doc  = sum([len(doc) for doc in test_doc.values()])
    
    train_vsm       = VSM(train_doc ,doc_frq ,total_train_doc)
    
    test_vsm        = VSM(test_doc ,doc_frq ,total_train_doc)

    predict_output  = ApplyKNN(test_vsm,train_vsm,K)
    
    accuracy        = (sum(predict_output.values())/total_test_doc)*100
    
    print('ACCURACY : ',accuracy,' %')


def KNNDriver(ratio,K):
    print('IN K-NN')
    
    test_doc , train_doc, doc_frq , actual_output  = ReadFile(ratio)
    
    total_train_doc = sum([len(doc) for doc in train_doc.values()])
    total_test_doc  = sum([len(doc) for doc in test_doc.values()])
    
    print('READING PART DONE...')

    train_vsm       = VSM(train_doc ,doc_frq ,total_train_doc)
    
    test_vsm        = VSM(test_doc ,doc_frq ,total_train_doc)

    print('VECTOR PART DONE...')

    predict_output  = ApplyKNN(test_vsm,train_vsm,K)
    
    accuracy        = (sum(predict_output.values())/total_test_doc)*100
    
    print('ACCURACY : ',accuracy,' %')

    return accuracy

    