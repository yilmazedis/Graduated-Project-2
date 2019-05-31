from array import array

with open("outputs") as f:
    content = f.readlines()

content = [int(x.strip()) + 1 for x in content]

output_file = open('file', 'wb')
float_array = array('d', content)

float_array.tofile(output_file)
output_file.close()
