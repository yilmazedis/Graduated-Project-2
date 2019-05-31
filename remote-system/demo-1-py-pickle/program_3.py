import pickle
from zipfile import ZipFile 
import os 


with open('outputs.pickle', 'rb') as handle:
    inputs = pickle.load(handle)


result = [1 + int(i) for i in inputs]


print(result)


with open('outputs', 'w') as f:
    for item in result:
        f.write("%s\n" % item)


with ZipFile('outputs.zip','w') as zip: 
    zip.write("outputs") 

os.remove("outputs")