import json
import sys


f = open(sys.argv[1], 'r')
data = json.load(f)
print(len(data))
