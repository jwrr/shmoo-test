
# # utils.py

import sys
import re


def isint(s):
  try:
    int(s)
  except ValueError:
    return False
  return True


def isfloat(s):
  try:
    float(s)
  except ValueError:
    return False
  return True


def ishex(s):
  s = s.lower()
  if not s.startswith('0x'):
    return False
  s = s[2:]
  try:
    int(s, 16)
  except ValueError:
    return False
  return True


def allints(l):
  return all(isint(s) for s in l)


def allfloats(l):
  return all(isfloat(s) for s in l)


def allhexs(l):
  return all(ishex(s) for s in l)


def tofloat(s):
  try:
    return float(s)
  except ValueError:
    return s


def toint(s):
  try:
    return int(s)
  except ValueError:
    return s


def tohexint(s):
  try:
    return int(s, 16)
  except ValueError:
    return s


def istrue(s):
  return s.lower() in ['true', 'on', 'yes', 'y']


def isfalse(s):
  return s.lower() in ['false', 'off', 'no', 'n']


def isbool(s):
  return istrue(s) or isfalse(s)


def tobool(s):
  return istrue(s)


def slurplines(filename):
  lines = []
  with open(filename, 'r') as f:
    lines = f.read().splitlines()
  return lines


def removecomments(lines, commentstart='#'):
  return [re.sub(commentstart + '.*', '', s) for s in lines]


def removeblanks(lines):
  return list(filter(None, lines))


def combinelines(lines, marker="'''"):
  olines = []
  combine = False
  oline = ''
  for line in lines:
    markerfound = marker in line
    if markerfound:
      line = line.replace(marker, '')
    if combine:
      oline = oline + line + '\n'
    else:
      oline = line
    if markerfound:
      combine = not combine
    if not combine:
      olines.append(oline)
      oline = ''
  return olines


def longestkey(d):
  klen = 0
  for k,v in d.items():
    if len(k) > klen:
      klen = len(k)
  return klen


def strkv(d, name = '', sep='\n', skip={}, firstcol=0):
  klen = longestkey(d) + len(name) + 2
  printlist = []
  for k,v in d.items():
    if type(v) == list and firstcol>0:
      v = v[firstcol:]
    if k not in skip:
      if name != '':
        k = f'{name}[{k}]'
      if sep == '\n':
        k = k.ljust(klen)
        s = f'{k} = {v}'
      else:
        s = f'{k}={v}'
      printlist.append(s)
  return sep.join(printlist)


def replacewithkv(s, d, pre='', post=''):
  for k,v in d.items():
    fromstr = pre + str(k)  + post
    tostr = str(v)
    s = s.replace(fromstr, tostr)
  return s


def stripall(lines):
  return [s.strip() for s in lines]


def dbg(s):
  print(s, file=sys.stderr)

def abort(s='', err=1):
  dbg(f'Error {err}: {s}', file=sys.stderr)
  sys.exit(err)


def getorquit(d,k):
  if k not in d:
    utils.abort(f"'{k}' not defined")
  return d[k]


def first(od):
  return next(iter(od.items()))


def get_nth(od, n):
  if n > len(od)-1:
    return
  k = list(od.keys())[n]
  v = od[k]
  return k,v
