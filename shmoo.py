#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
from collections import OrderedDict
from decimal import *
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
  
  current, first, last, step = r
  seq = [current]
  done = (step == 0)
  if done:
    seq.append(first)
  while not done:
    seq.append(current)
    current = current + step
    done = (step > 0) and (current > last) or (step < 0) and (current < last)
  return seq


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
    v = 'True' if numparts == 1 else parts[1].strip()
    seq = expandrange(v)
    cfg[k].extend(seq)
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


def run(cfg, depth=0, cnt=0):
  done = depth >= len(cfg)-1
  if done:
    cnt += 1
    currcfg = getcurrent(cfg)
    s = f'# {cnt}: ' + utils.strkv(currcfg, '', ',', dict(template=1))
    print(s)
    template = utils.replacewithkv(currcfg['template'], currcfg, '{', '}')
    print(template)
    print('')
    return cnt
  k,v = utils.get_nth(cfg, depth)
  for current in v[1:]:
    cfg[k][0] = current
    cnt = run(cfg, depth+1, cnt)
  return cnt


def getcurrent(cfg):
  curr = {}
  for k in cfg:
    curr[k] = cfg[k][0]
  return curr


# ==============================================================
# ==============================================================


cfg = setup()
s = utils.strkv(cfg, '', '\n', {}, 1)
utils.dbg(s)
cnt = run(cfg)

