#!/usr/bin/env python3
# shmoo.py
# python3 shmoo.py

import sys
import re
import random
from collections import OrderedDict
import utils


def fakegaussian(first, last, cnt=2):
  centrallimit = sum( [random.uniform(first, last) for i in range(cnt)] ) / cnt
  return centrallimit


def sweeprange(rangelist):
  first, last, step = rangelist
  seq = []
  done = (step == 0)
  if done:
    seq.append(first)
  current = first
  cnt = 0
  while not done:
    seq.append(current)
    cnt += 1
    current = first + cnt*step
    done = (step > 0) and (current > last) or (step < 0) and (current < last)
  return seq


def distrange(dist, rangelist):
  dist = dist.lower()
  first, last, cnt = rangelist
  scale = utils.getmaxscale([first, last])
  seq = []
  if dist == 'lin':
    m = (last - first) / (cnt-1)
    b = first
    for x in range(cnt):
      seq.append( round(m*x + b, scale) )
  elif dist == 'log':
    y = last / first
    nthroot = cnt-1
    b = y**(1/nthroot)
    a = first
    for x in range(int(cnt)):
      seq.append( round(a*b**x, scale) )
  elif dist == 'rand':
    random.seed()
    for x in range(int(cnt)):
      seq.append( round(random.uniform(first, last), scale) )
  elif dist == 'norm':
    random.seed()
    for x in range(int(cnt)):
      seq.append( round(fakegaussian(first, last), scale) )
  return seq


def expandrange(rstr):
  distributions = dict(lin=1, log=2, rand=3, norm=4, bin=5)
  parts = utils.stripall(rstr.split(':'))
  isdist = parts[0].lower() in distributions.keys()
  dist = parts.pop(0) if isdist else ''
  rangelist = utils.settype(parts)
  rlen = len(rangelist)
  if rlen == 1:
    rangelist.append(rangelist[0]) # last = first
    rangelist.append(0)    # step or cnt = 0
  elif rlen == 2:
    rangelist.append(1)    # step or cnt = 1
  seq = distrange(dist, rangelist) if isdist else  sweeprange(rangelist)
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
