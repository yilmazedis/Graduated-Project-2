with open("outputs") as f:
    content = f.readlines()

content = [int(x.strip()) + 1 for x in content] 

with open('outputs', 'w') as f:
    for item in content:
        f.write("%s\n" % item)