# shmoo.py
# python3 shmoo.py

import sys
from collections import OrderedDict


def getargs(cfg):
  prog = sys.argv[0]
  args = sys.argv[1:]
  for arg in args:
    parts = arg.split('=',1)
    numparts = len(parts)
    k = parts[0]
    if numparts == 1:
      cfg[k] = True
    else:
      v = parts[1]
      vparts = v.split(':',2)
      if (not isfloat(vparts[0])):
        cfg[k] = v
      else:
        vfloats = res = [tofloat(s) for s in vparts]
        cfg[k] = vfloats
  return cfg

def isfloat(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def tofloat(s):
  try:
    return float(s)
  except ValueError:
    return s

def printkv(d, name=''):
  for k,v in d.items():
    print(f'cfg[{k}] = {v}')

def replace(t, d):
  for k,v in d.items():
    fromstr = '{' + str(k)  + '}'
    tostr = str(v)
    t = t.replace(fromstr, tostr)
  return t

cfg = OrderedDict(
  filter     = 15,
  infreq     = 10,
  tunefreq   = 10,
  iamp       = 100,
  qamp       = 100,
  track      = True,
  )

template = '''
  run_script {filter} {infreq} {tunefreq} {iamp} {qamp} track
'''

cfg = getargs(cfg)
printkv(cfg)

print(template)
template = replace(template, cfg)
print(template)






