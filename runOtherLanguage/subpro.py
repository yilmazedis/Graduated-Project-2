import subprocess

# for run python codes
""" 
inp = '[1,2,3,55,6,23,[432, 3,3]]'.encode('utf-8')

result = subprocess.run(['python', 'helloworld.py'], stdout=subprocess.PIPE, input=inp)

print(result.stdout.decode('utf-8'))
"""

# for run c codes

inp = '100 12 234 2 4 2 1'.encode('utf-8')

subprocess.run(['gcc', '-o', 'hello', 'helloworld.c'], stdout=subprocess.PIPE)

result = subprocess.run(['hello'], stdout=subprocess.PIPE, input=inp)

print(result.stdout.decode('utf-8'))
