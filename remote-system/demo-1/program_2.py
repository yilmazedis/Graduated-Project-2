import pickle

with open('outputs.pickle', 'rb') as handle:
    inputs = pickle.load(handle)


result = [1 + int(i) for i in inputs]


print(result)


with open('outputs.pickle', 'wb') as output_file:
	pickle.dump(result, output_file, protocol=pickle.HIGHEST_PROTOCOL)