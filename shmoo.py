#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
from collections import OrderedDict
from decimal import *
import utils


def sweeprange(rangelist):
  first, last, step = rangelist
  seq = []
  done = (step == 0)
  if done:
    seq.append(first)
  current = first
  while not done:
    seq.append(current)
    current = current + step
    done = (step > 0) and (current > last) or (step < 0) and (current < last)
  return seq


def expandrange(rstr):
  parts = utils.stripall(rstr.split(':',2))
  rangelist = utils.settype(parts)
  rlen = len(rangelist)
  if rlen == 1:
    rangelist.append(rangelist[0]) # last = first
    rangelist.append(0)    # step = 0
  elif rlen == 2:
    rangelist.append(1)    # step = 1
  seq = sweeprange(rangelist)
  return seq

def expandlist(lstr):
  parts = utils.stripall(lstr.split(',',2))
  seq = [0] # first item will be used as 'current' value
  for rstr in parts:
    rseq = expandrange(rstr)
    seq.extend(rseq)
  if len(seq) > 1:
    seq[0] = seq[1]
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
    v = parts[1].strip() if len(parts) > 1 else 'True'
    seq = expandlist(v)
#   seq = expandrange(v)
    cfg[k] = seq
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
    utils.dbg(s)
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


def main():
  cfg = setup()
  s = utils.strkv(cfg, '', '\n', {}, 1)
  utils.dbg(s)
  cnt = run(cfg)


main()
