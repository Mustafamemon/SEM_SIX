import os
import re
import json
import math
import numpy 
import statistics
from random import randint,seed , shuffle
from collections import Counter
from StemmingWord import StemmingWord

seed(1)
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

def ReadFile():
    folder_path = os.path.abspath('bbcsport')
    
    content        = ""
    doc_frq        = {}
    all_doc        = []
    
    for nested_folder_path, subdirs, files in os.walk(folder_path):
        all_vocab  = []
        if len(subdirs) is 0:
            _class     = os.path.basename(nested_folder_path)
            for file_path in files:
                file           = open(nested_folder_path +'\\'+ file_path , "r")
                
                content        =  file.read()
                
                r_stop_word    = clean(content)
                stem_vocab     = StemmingWord(r_stop_word)
        
                doc_count      = {}
                doc_count      = doc_count.fromkeys(stem_vocab,1)
                
                doc_frq        = Counter(doc_frq) + Counter(doc_count)
                
                all_doc.append([_class]+stem_vocab)

    filter_doc_frq  = {}
    for (k,v) in doc_frq.items():
        if v >= 3:
            filter_doc_frq[k] = v
        
    return (all_doc,filter_doc_frq)

def VSM(all_doc ,doc_frq):
    total_doc = len(all_doc)
    vsm       = [] 
    vocab     = doc_frq.keys()
    for doc_vocab in all_doc:
        doc_vector = []
        doc_vector = [doc_vocab.count(word)*math.log10(total_doc/ doc_frq[word]) for word in vocab]
        vsm.append([doc_vocab[0]] +  doc_vector)

    file_path = os.path.abspath("")
    save_file = {'vsm':vsm,}
    dict = json.dumps(save_file)
    file = open(file_path+'\KMeanIndex.json','w')
    file.write(dict)
    file.close()

    return vsm

def CosineSimilarity(x,y):
    x_dot_y = numpy.dot(x,y)
    mag_x   = numpy.linalg.norm(x)
    mag_y   = numpy.linalg.norm(y)
    
    return x_dot_y / (mag_x*mag_y)
   
def EuclideanDistance(x,y):
    x = numpy.array(x)
    y = numpy.array(y)
    return numpy.linalg.norm(x - y).item()

def Centriod(cluster):
    cluster       = numpy.array(cluster)
    length, dim   = cluster.shape
    
    return numpy.array([numpy.sum(cluster[:, i])/length for i in range(dim)]).tolist()
    
def ApplyKMean(vsm,K):
    iteration = 0
    if K < len(vsm):
        prev_centriod = []
        
        centriod      = vsm[:K]
        centriod      = numpy.delete(centriod, 0, axis=1).astype('float64').tolist()
        
        
        while prev_centriod != centriod:
            iteration  +=  1

            cluster     = [[] for k in range(0,K)]
            ans_cluster = [[] for k in range(0,K)]
        
            for vector in vsm:
                x = numpy.delete(vector, 0, axis=0).astype('float64').tolist()
                distance = []
                for y in centriod:
                    distance.append(CosineSimilarity(x,y))
                
                index = distance.index(max(distance))
                
                cluster[index].append(x)
            
                ans_cluster[index].append(vector[0])
                
            prev_centriod = centriod
            centriod      = []
            
            for i in range(0,len(cluster)):
                
                if len(cluster[i]) == 0:
                    ind = randint(0,len(vsm)-1)
                    x = numpy.delete(vsm[ind], 0, axis=0).astype('float64').tolist()
                    cluster[i].append(x)
                    
                centriod.append(Centriod(cluster[i]))
            
            print('Done With Iteration # ',iteration)

        
        return ans_cluster
def Purity(cluster,features):
    max_count = []
    for c in cluster:
        max_count.append(c.count(statistics.mode(c)))
    
    purity = 1/features * sum(max_count)

    return purity

if __name__ == "__main__":
    all_doc , doc_frq  = ReadFile()
    vsm                        = VSM(all_doc ,doc_frq)
    
    filepath = file_path = os.path.abspath("KMeanIndex.json")
    if os.path.exists(filepath):
        if os.stat(filepath).st_size != 0:
            with open(filepath) as f:
                dict     = json.load(f)
                vsm      = dict['vsm']
            f.close()  
    shuffle(vsm)
    features      = len(vsm)
    vsm           = numpy.array(vsm)
    
    cluster       = ApplyKMean(vsm,5)
    purity        = Purity(cluster,features)
    
    for c in cluster:
        print(c,end='\n\n\n')
    
    print('Purity : ',purity)


def KMeanDriver():
    print('IN K-MEAN')
    filepath = file_path = os.path.abspath("KMeanIndex.json")
    if os.path.exists(filepath):
        if os.stat(filepath).st_size != 0:
            with open(filepath) as f:
                dict     = json.load(f)
                vsm      = dict['vsm']
            f.close()  
    else:
        all_doc , doc_frq  = ReadFile()
        vsm                = VSM(all_doc ,doc_frq)
    
    shuffle(vsm)

    print('READING FILE AND VECTOR DONE')

    features      = len(vsm)
    vsm           = numpy.array(vsm)
    
    cluster       = ApplyKMean(vsm,5)
    purity        = Purity(cluster,features)
    
    # for c in cluster:
        # print(c,end='\n\n\n')
    
    print('Purity : ',purity)
    return purity