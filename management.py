import math
import copy

totalInput = 22
power = [10, 15, 30, 20]
allpower = sum(power)

inputs = {
	"input" : {
	}
}

for inp in range(totalInput):
	inputs["input"][str(inp)] = [inp]

#print(inputs)

hak = []
for p in power:
	hak.append(math.ceil((p * totalInput) / allpower))

print("hak: ", hak)
print("sum of hak: ", sum(hak))

sortedHak = copy.deepcopy(hak)

sortedHak = sorted(hak,reverse=True)

print("sorted Hak: ", sortedHak)

 
sortedIndex = sorted(range(len(hak)), reverse=True, key=hak.__getitem__)

while sum(sortedHak) != totalInput:
	for i in range(len(hak)):
		if sortedHak[i] != 1 and sum(sortedHak) != totalInput:
			sortedHak[i] -= 1

print("modified sortedHak: ", sortedHak)
print("sum of modified sortedHak: ", sum(sortedHak))
print("sortedIndex: ", sortedIndex)

actualCase = [y for y, x in sorted(zip(sortedHak, sortedIndex))]

print("actual case: ", actualCase)

preKey = "0"
actualIndex = 1
for share in actualCase:
	keys = [key for key in range(int(preKey),int(share) + int(preKey) )]
	filtered = dict(zip(keys, [inputs["input"][str(k)] for k in keys]))
	preKey = sum(actualCase[0:actualIndex])
	actualIndex += 1
	print(filtered)
	print()

