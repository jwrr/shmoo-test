#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
from collections import OrderedDict


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

def parsecfg(args):
  cfg = OrderedDict()
  arg = ''
  for arg in args:
    parts = arg.split('=',1)
    numparts = len(parts)
    k = parts[0].strip()
    if numparts == 1:
      cfg[k] = True
    else:
      v = parts[1].strip()
      vparts = stripall(v.split(':',2))
      first = vparts[0]
      if isbool(first):
        cfg[k] = tobool(first)
      elif first.isnumeric():
        cfg[k] = [tofloat(s) for s in vparts]
      else:
        cfg[k] = v
  return cfg

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

def readcfg(filename):
  lines = slurplines(filename)
  lines = combinelines(lines, "'''")
  lines = removecomments(lines)
  lines = removeblanks(lines)
  cfg = parsecfg(lines)
  return cfg

def setup():
  args = parsecfg(sys.argv[1:])
  filename = 'shmoo.cfg'
  if 'cfg' in args:
    filename = args['cfg']
  cfg = readcfg(filename)
  cfg.update(args)
  return cfg

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

def replace(t, d):
  for k,v in d.items():
    fromstr = '{' + str(k)  + '}'
    tostr = str(v)
    t = t.replace(fromstr, tostr)
  return t

def abort(s='', err=1):
  print(f'Error: {s}', file=sys.stderr)
  sys.exit(err)


# def recurse(template, cfg, i=0):
#   if i in cfg.items()[i]

# ==============================================================
# ==============================================================

cfg = setup()
printkv(cfg)

if 'template' not in cfg:
  abort("'template' not defined")

template = cfg['template']
print("============================")
print(template)
template = replace(template, cfg)
print("============================")
print(template)

i = 0

# recurse(template, cfg)
