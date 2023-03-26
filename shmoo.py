#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
from collections import OrderedDict

import utils

def parse(args):
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
      vparts = utils.stripall(v.split(':',2))
      numvparts = len(vparts)
      first = vparts[0]
      if numvparts == 2:
        vparts[2] = 1
      if numvparts == 3:
        if utils.isint(first):
          cfg[k] = [utils.toint(s) for s in vparts]
        elif utils.isfloat(first):
          cfg[k] = [utils.tofloat(s) for s in vparts]
        elif utils.ishex(first):
          cfg[k] = [utils.tohexint(s) for s in vparts]
        else:
          cfg[k] = v
      else:
        s = first
        if utils.isint(first):
          cfg[k] = utils.toint(s)
        elif utils.isfloat(first):
          cfg[k] = utils.tofloat(s)
        elif utils.ishex(first):
          cfg[k] = utils.tohexint(s)
        else:
          cfg[k] = v
  return cfg

def readcfg(filename):
  lines = utils.slurplines(filename)
  lines = utils.combinelines(lines, "'''")
  lines = utils.removecomments(lines)
  lines = utils.removeblanks(lines)
  cfg = parse(lines)
  return cfg

def setup():
  args = parse(sys.argv[1:])
  filename = 'shmoo.cfg'
  if 'cfg' in args:
    filename = args['cfg']
  cfg = readcfg(filename)
  cfg.update(args)
  return cfg

def recurse(template, cfg, i=0, cnt=0):
  k,v = utils.get_nth(cfg, i)

  print(f'dbg {i}: key={k}, value={v}')
  
  if type(v) == list:
    first, last, step = v
    current = first
    epsilon = 0.00001
    while current <= last+epsilon:
#     print(f'dbg first={first}, last={last}, incr={step}')
      cfg[k] = current
      if i < len(cfg)-1:
        cnt = recurse(template, cfg, i+1, cnt)
      else:
        print("dbg DONE1!!!!!!")
        utils.printkv(cfg, '', ',')
        cnt += 1
      current += step
    return cnt
  else:
#     print(f'dbg constant={const}')
    if i < len(cfg)-1:
      cnt = recurse(template, cfg, i+1, cnt)
    else:
      print("dbg DONE2!!!!!!")
      utils.printkv(cfg, '', ',')
      cnt += 1
      return cnt
  return cnt


# ==============================================================
# ==============================================================

cfg = setup()
utils.printkv(cfg, 'cfg', '\n')

template = utils.getorquit(cfg, 'template')
print("============================")
print(template)
template = utils.replacewithkv(template, cfg, '{', '}')
print("============================")
print(template)

i = 0

cnt = recurse(template, cfg)

print(f'{cnt} test conditions created')

