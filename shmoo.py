#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
from collections import OrderedDict
import utils


def expandrange(rstr):
  vparts = utils.stripall(rstr.split(':',2))
  numvparts = len(vparts)
  first = vparts[0]
  r = [0]
  if numvparts == 2:
    vparts[2] = 1
  if utils.allints(vparts):
    r.extend( [utils.toint(s) for s in vparts] )
  elif utils.allfloats(vparts):
    r.extend( [utils.tofloat(s) for s in vparts] )
  elif utils.allhexs(vparts):
    r.extend( [utils.tohexint(s) for s in vparts] )
  else:
    r.append(rstr)
  rlen = len(r)
  r[0] = r[1]      # current = first
  if rlen == 2:
    r.append(r[1]) # last = first
    r.append(0)    # step = 0
  elif rlen == 3:
    r.append(1)    # step = 1
  return r


# arg=99,0.1:0.9:0.2,1:9:2,10:90:20
# arg=a,b,c,d,e
# a=5 or a=1:10 or a=2:10:1
def parse(args):
  cfg = OrderedDict()
  arg = ''
  for arg in args:
    parts = arg.split('=',1)
    numparts = len(parts)
    k = parts[0].strip()
    cfg[k] = []
    if numparts == 1:
      cfg[k].append(True)
      cfg[k].append(True)
      cfg[k].append(True)
      cfg[k].append(True)
    else:
      v = parts[1].strip()
      r = expandrange(v)
      cfg[k].extend(r)
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


def recurse(cfg, depth=0, cnt=0):
  if depth >= len(cfg)-1:
    cnt += 1
    currcfg = getcurrent(cfg)
    s = f'\n# {cnt}: ' + utils.strkv(currcfg, '', ',', dict(template=1))
    print(s)
    template = utils.replacewithkv(currcfg['template'], currcfg, '{', '}')
    print(template)
    return cnt
  k,v = utils.get_nth(cfg, depth)
  print(f'dbg {depth}: key={k}, value={v}')
  current, first, last, step = v
  if step == 0:
    cnt = recurse(cfg, depth+1, cnt)
  else:
    current = first
    cfg[k][0] = current
    epsilon = 0.00001
    while current <= last+epsilon:
      cnt = recurse(cfg, depth+1, cnt)
      current += step
      cfg[k][0] = current
  return cnt


def getcurrent(cfg):
  curr = {}
  for k in cfg:
    curr[k] = cfg[k][0]
  return curr


# ==============================================================
# ==============================================================


cfg = setup()
print(cfg)
currcfg = getcurrent(cfg)
print(currcfg)

# print( utils.strkv(currcfg, 'cfg', '\n', {'template':1}) )
# template = utils.getorquit(currcfg, 'template')
# print("============================")
# print(template)
# template = utils.replacewithkv(template, currcfg, '{', '}')
# print("============================")
# print(template)

cnt = recurse(cfg)

