
## shmoo-test

In electronics, shmoo testing (or shmooing) is the process running the same 
test over many different conditions, to identify where the boundary conditions 
wherein the component will work.  Commonn parameters to vary are Power Supply 
Voltage, Ambient Temperature and Clock Frequency.
Status

## Status

Alpha. It works for me.


## Dependencies

Python3 (tested with v3.8)


## Why?

We needed to a run a test under many electrical and environmental conditions, 
to find out under what conditions a device worked. So we wrote `shmoo.py` to 
sweep through all permutations of several parameters, and create a test for 
each configuration of parameters.


## Example

Here is an exmple to create tests that sweep over four variable rangess. Each
Variable Range Definition (VRD) consists of a range name, an equal sign ('='), 
and a range of values. Note there aren't any spaces in a VRD, but each
VRD is separated by a space.

```bash
./shmoo.py clk_freq=100 p=tt,ss,ff v=1.0:1.5:0.1 t=-5:5:5,25:35:5,65:75:5
```

The first VRD is `clk_freq=100`, where the range name is `clk_freq`. The 
range name can be prety much any name you want. For this VRD the range is a
single value, `100`. A single value range means the variable will always have 
that value for all test case permutations.

The second VRD is `p=tt,ss,ff`, where the range name is `p` and the range is
`tt,ss,ff`. A comma separated range is a list of possible values. So in this
case the `p` variable will sweep over the three values `tt`, 'ss' and 'ff'. In
this case the list values are strings, but the list values can also be numeric.

The third VRD is `v=1.0:1.5:0.1`, where the range name is `v` and the range is
`.0:1.5:0.1`. A colon separated range generates a sequence of values, where the
sequence starts at the first value, ends at the second value (inclusive), with a
step size of the third value. In this example the range will cover the following
five values: 1.0, 1.1, 1.2, 1.3, 1.4 and 1.5.

The fourth VRD is `t=-5:5:5,25:35:5,65:75:5`, where the range name is `t` and the range
is a combination of a several colon lists, where the `t` variable sweeps through
the nine values -5, 0, 5, 25, 30, 35, 65, 70 and 75.

The above simple example will generate 135 test case permutatations (1 * 3 * 5 * 9).


## Variable Parameters

The command line parameters are user defined, space separated, key-value pairs.
The key can be pretty much any name that describes your parameter. The key and
value are separated by an `=` equal sign. The value can be a constant, comma 
separated list or colon separated range. 


Here are some more parameter examples.

```bash
a=5 # constant
b=10:20 # range with step size of 1
c=100:1000:100 # range with step size of 100
d=[LIN,LOG,RAND,GAUSSIAN,BINO]:1:1000:50
e=LIN:1:1000:50   # linear slope with 50 values
f=LOG:1:1000:50   # exponential slope
g=RAND:1:1000:50  # uniform random distribution
h=NORM:1:1000:50  # guassian distribution
i=BINO:10:20:50   # binomial distribution (tbd)
```

* `a` is set to a constant value of 5.
* `b` is set to a range from 10 to 20 inclusive with a default step size of 1.
* `c` is set to a range from 100 to 1000 inclusive with a step sof of 100.
* `e` is set to a linear slope from 1 to 100 inclusive, with 50 steps.
* `f` is set to a logarithmic/exponential slope from 1 to 1000 with 50 steps.
* `g` is set to a random uniform distribution of 50 values in the range of 1 to 1000 (inclusive)
* `h` is set to a random gaussian distribution of 50 values in the range from 1 to 1000 (inclusive)


## The Template

The template contains your commands that your parameters are inserted into. 
The template can be defined on the command line with parameter `template` as 
shown in the following example. In this example, you create the executable
`run_test` (any name works) with four arguments.

```bash
python3 shmoo.py template='run_test {f} {p} {v} {t}' clk_freq=100 p=tt,ss,ff v=1.0:1.5:0.1 t=-5:5:5,25:35:5,65:75:5
```

Each variable is enclosed in a pair of curly braces, `{}`, similar to Python's
f-string. For multi-line templates a `\n` separates the lines.  When the 
template is defined in the configuration file, multi-line templates can be 
enclosed in triple quotes, similar to Python's triple-quote.

##Configuration File

The configuration file is optional and contains default values for the
parameters. The default file name is `schmoo.cfg`, and can be redefined on the 
command line with the `cfg=xyz.txt` parameter.

Here is an example config file.

```bash
name=trial42 # comments can be on same line too
p=tt
v=3.3
t=20
f1=100
f2=100
```

The triple-quote can be used for multi-line commands templates

```
template = '''
run_test {p} {v} {t} {f1} {f2}
cp results.txt to {name}_{p}_{v}_{t}_{f1}_{f2}.txt
'''
```

## Output

The output of `shmoo.py` is an executable text file that can be run from the 
command line. The output goes to `stdout` and is typically redirected to a 
file with the Unix `>' redirect.


## Example Run

Here is an example run

```bash
./shmoo.py  t=-4:4:1,18:22:2,90:110:5 > runscript.sh
```

and the resulting output file is:

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
