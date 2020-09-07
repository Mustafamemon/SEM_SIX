import lematization as l
from reading_file import file_path , readFile
import os
import json
import math



def Query(query):
    filepath = file_path + '\index.json'
    if os.path.exists(filepath):
        if os.stat(filepath).st_size != 0:
            with open(filepath) as f:
                dic = json.load(f) 
            f.close()  
    else:
        print('if index.json not exist')
        readFile()
        with open(filepath) as f:
            dic = json.load(f) 
        f.close()  
    stop_word       = dic['stop_word']
    VSM             = dic['VSM']
    doc_frq         = dic['doc_frq']
    vocab           = dic['vocab'],
    
    query           = query.split(' ')
    query           = [x.lower() for x in query]
    stop_word_query = list(set(query) - set(stop_word))
    lema_query      = l.lematization_word(stop_word_query)
    queryDict       = {}
    queryDict       = queryDict.fromkeys(lema_query,0)

    for j in range(0,len(lema_query)):
        queryDict[lema_query[j]] = queryDict[lema_query[j]] + query.count(stop_word_query[j])

    for word in lema_query:
        try:
            queryDict[word] = queryDict[word]*math.log10(56 / doc_frq[word])
        except ( KeyError , ZeroDivisionError) :
            queryDict[word] = 0.0
    ans = []
    for doc_no in range(0,56):
        _sum = 0.0
        for word in lema_query:
            try:
                _sum = _sum + (VSM[doc_no][word] * queryDict[word]) 
            except KeyError:
                _sum = _sum + (0.0 * queryDict[word])
    
        x = [ v for k, v in VSM[doc_no].items()] 
        y = [ v for k, v in queryDict.items()] 
        
        mag_x = math.sqrt(sum(x_i*x_i for x_i in x))
        mag_y = math.sqrt(sum(y_i*y_i for y_i in y))
        try:
            sim   =  _sum/(mag_x*mag_y)
        except ZeroDivisionError:
            return 0
        if sim >=0.0005:
            ans.append((sim,doc_no))
            # print('doc_no : ',doc_no,end=' -> ')
            # print('SIM : ',sim)
    
    ans  = sorted(ans,reverse=True)
    
    output = [item[1] for item in ans] 
    print(output)
    print('LENGTH : ',len(ans))
    return output
