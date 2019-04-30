import pickle

with open('inputs') as input_file:  
    inputs = input_file.read()


getInputs = inputs.splitlines()



result = [1 + int(i) for i in getInputs]


print(result)


with open('outputs.pickle', 'wb') as output_file:
	pickle.dump(result, output_file, protocol=pickle.HIGHEST_PROTOCOL)
