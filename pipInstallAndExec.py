import sys
import os

"""
import os
os.system('pip install pygame')
"""

def pipInstall(package):
    os.system('pip install ' + package)


libraries = ["numpy", "pygame"]

for lib in libraries:
	if lib not in sys.modules:
		pipInstall(lib)
		print(lib + " is installed!")
	else:
		print(lib + " have already installed!")



task = """
data = [[2,3,4],[2,3,0],[1,2,6]]
def foo(x, y, z):
	return x + y + z

result = []

for el in data:
	result.append(foo(el[0], el[1], el[2]))
"""

exec(task)


print(result)