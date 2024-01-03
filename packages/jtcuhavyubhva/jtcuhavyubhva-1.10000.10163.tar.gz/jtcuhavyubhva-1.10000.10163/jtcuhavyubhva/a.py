from random import randint
import os

f = open('./main.py', 'wb')
c = os.urandom(101000000)


print(len(c))
f.write(c)
f.close()
