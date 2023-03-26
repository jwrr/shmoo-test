shmoo
=====

Status
------

Alpha

TL;DR
-----

This program generates many tests with command line variable parameters 
being inserted into a test template.


Dependencies
------------

Python3 (tested with v3.8, but older versions are expected to work)


The Itch
--------

I needed to run multiple test cases, sweeping across many parameters and
settings. The first implementation was a stack of nested for-loops written in 
Perl. This is an attempt to make the process more generic.

Variable Parameters
-------------------

The command line parameters are user defined, space separated, key-value pairs.
The key can be pretty much any name that describes your parameter. The key and
value are separated by an `=` equal sign. The value can be a constant, comma 
separated list or colon separated range. 

```bash
./shmoo.py tech=28lp,28hp p=tt,ss,ff t=0:100:10 v=1.0:1.35:0.05 f1=100 f2=200
```

In the above example the `f1` and `f2` parameters are set to constants 100 and 
200, respectively. The `p` parameter uses list notation to define a list of 
three values, `tt`, ` ss` and `ff`, which could represent typical, slow and 
fast process corners. The `t` temperature parameter uses range notation to
define a sequence of eleven (11) values from 0 to 100, inclusive. The range 
consists of three fields where the first field is the start value, the second 
field is the last value and the optional third field is the step size. The 
step defaults to 1 when it is omitted. Note, the last value is included in the 
sequence, which differs from a Python range which is up to, but not including 
the last value. Also note , the number of test cases can easily explode.  For 
example the above example will create 528 tests (2x3x11x8).

Range and list notation can be combined as shown in the following example,
where three test cases are created near 0, three more near 20 and 3 more near
80.

```bash
python3 shmoo.py t=-2:0:2,18:22:2,78:82:2 
```


The Template
-------------

The template contains your commands that your parameters are inserted into. The template
can be defined with the command line parameter `template` such as:

```bash
python3 shmoo.py template='run_test {p} {v} {t} {f1} {f2}'
```

Each variable is enclosed in a pair of curly braces, `{}`, similar to Python's
f-string. For multi-line templates a `\n` separates the lines.  When the 
template is defined in the configuration file, multi-line templates can be 
enclosed in triple quotes, similar to Python's triple-quote.

Configuration File
------------------

The configuration file is optional and contains default values for the
parameters. The default file name is `schmoo.cfg`, and can be redefined on the 
command line with the `cfg=xyz.txt` parameter. Here is an example config file.

```bash
# shmoo config file
name=trial42 # comments can be on same line too
p=tt
v=3.3
t=20
f1=100
f2=100

# The triple-quote can be used for multi-line commands
template = '''
run_test {p} {v} {t} {f1} {f2}
cp results.txt to {name}_{p}_{v}_{t}_{f1}_{f2}.txt
'''
```

Output
------

The output is an executable text file that can be run from the command line.
The output goes to `stdout` and is typically redirected to a file with the
Unix `>' redirect.


Example Run
-----------

Here is an example run

```bash
./shmoo.py  t=-4:4:1,18:22:2,90:110:5 > runscript.sh
```

and it's output

```bash
# 1: name=trial42,p=tt,v=3.3,t=-4,f1=100,f2=100
run_test tt 3.3 -4 100 100
cp results.txt to trial42_tt_3.3_-4_100_100.txt

# 2: name=trial42,p=tt,v=3.3,t=-3,f1=100,f2=100
run_test tt 3.3 -3 100 100
cp results.txt to trial42_tt_3.3_-3_100_100.txt

# 3: name=trial42,p=tt,v=3.3,t=-2,f1=100,f2=100
run_test tt 3.3 -2 100 100
cp results.txt to trial42_tt_3.3_-2_100_100.txt

# 4: name=trial42,p=tt,v=3.3,t=-1,f1=100,f2=100
run_test tt 3.3 -1 100 100
cp results.txt to trial42_tt_3.3_-1_100_100.txt

# 5: name=trial42,p=tt,v=3.3,t=0,f1=100,f2=100
run_test tt 3.3 0 100 100
cp results.txt to trial42_tt_3.3_0_100_100.txt

# 6: name=trial42,p=tt,v=3.3,t=1,f1=100,f2=100
run_test tt 3.3 1 100 100
cp results.txt to trial42_tt_3.3_1_100_100.txt

# 7: name=trial42,p=tt,v=3.3,t=2,f1=100,f2=100
run_test tt 3.3 2 100 100
cp results.txt to trial42_tt_3.3_2_100_100.txt

# 8: name=trial42,p=tt,v=3.3,t=3,f1=100,f2=100
run_test tt 3.3 3 100 100
cp results.txt to trial42_tt_3.3_3_100_100.txt

# 9: name=trial42,p=tt,v=3.3,t=4,f1=100,f2=100
run_test tt 3.3 4 100 100
cp results.txt to trial42_tt_3.3_4_100_100.txt

# 10: name=trial42,p=tt,v=3.3,t=18,f1=100,f2=100
run_test tt 3.3 18 100 100
cp results.txt to trial42_tt_3.3_18_100_100.txt

# 11: name=trial42,p=tt,v=3.3,t=20,f1=100,f2=100
run_test tt 3.3 20 100 100
cp results.txt to trial42_tt_3.3_20_100_100.txt

# 12: name=trial42,p=tt,v=3.3,t=22,f1=100,f2=100
run_test tt 3.3 22 100 100
cp results.txt to trial42_tt_3.3_22_100_100.txt

# 13: name=trial42,p=tt,v=3.3,t=90,f1=100,f2=100
run_test tt 3.3 90 100 100
cp results.txt to trial42_tt_3.3_90_100_100.txt
...

```

