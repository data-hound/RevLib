import os
os.system('./1.py >tmp')
print(open('tmp', 'r').read())