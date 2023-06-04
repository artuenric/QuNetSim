import re
buffer = []
b = 91
regex = re.compile(r'.*\[[0-9]+\]$')
regex2 = fr'.*\[{b}\]$'
a = 'c8d2bd32-db4a-40d8-9ee0-3294cd321724[91]'
if re.fullmatch(regex2, a):
    print('True')
c = "c8d2bd32-db4a-40d8-9ee0-3294cd321724"
if re.fullmatch(regex2, a):
    buffer.append(a[:36])
if c in buffer:
    print("tá")