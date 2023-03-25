
# # utils.py

import sys
import re

def tofloat(s):
  try:
    return float(s)
  except ValueError:
    return s

def stripall(lines):
  return [s.strip() for s in lines]

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

def removecomments(lines):
  return [re.sub('#.*', '', s) for s in lines]

def removeblanks(lines):
  return list(filter(None, lines))

def combinelines(lines, marker="'''"):
  olines = []
  combine = False
  for line in lines:
    markerfound = re.search(marker, line)
    if markerfound:
      line = re.sub(marker, '', line)
    if combine:
      oline = oline + line + '\n'
    else:
      oline = line
    if markerfound:
      combine = not combine
    if not combine:
      olines.append(oline)
  return olines

def longestkey(d):
  klen = 0
  for k,v in d.items():
    if len(k) > klen:
      klen = len(k)
  return klen

def printkv(d, name=''):
  klen = longestkey(d) + 5
  for k,v in d.items():
    k = f'cfg[{k}]'
    k = k.ljust(klen)
    print(  f'{k} = {v}')

def replacewithkv(t, d, pre='', post=''):
  for k,v in d.items():
    fromstr = pre + str(k)  + post
    tostr = str(v)
    t = t.replace(fromstr, tostr)
  return t

def abort(s='', err=1):
  print(f'Error: {s}', file=sys.stderr)
  sys.exit(err)

def abortifundefined(d,k):
  if k not in d:
    utils.abort(f"'{k}' not defined")
  return d[k]


