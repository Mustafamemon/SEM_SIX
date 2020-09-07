file_path = "E:\Fast\SEM 6\IR\Assign - 2\index.json"
import re
import json
import os
import copy

def VSM():
    dict = {}
    if os.path.exists(file_path):
        if os.stat(file_path).st_size != 0:
            with open(file_path) as f:
                dict = json.load(f) 
                f.close()
    print(list(dict.keys()))

if __name__ == '__main__':
    VSM() 