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
      first = vparts[0]
      if utils.isbool(first):
        cfg[k] = utils.tobool(first)
      elif first.isnumeric():
        cfg[k] = [utils.tofloat(s) for s in vparts]
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

# def recurse(template, cfg, i=0):
#   if i in cfg.items()[i]

# ==============================================================
# ==============================================================

cfg = setup()
utils.printkv(cfg)

template = utils.abortifundefined(cfg, 'template')
print("============================")
print(template)
template = utils.replacewithkv(template, cfg, '{', '}')
print("============================")
print(template)

i = 0

# recurse(template, cfg)
