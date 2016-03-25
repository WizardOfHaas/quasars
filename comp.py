from os import listdir
from os.path import isfile, join
from astropy.io import fits
from scipy.interpolate import interp1d

import sys
import numpy as np
import pylab
import glob

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def normalize (a):
    return a / max(a)

#List of spectra to read...
spec_files = sys.argv[1:-1]

print spec_files
exit()

#Holder for composite spectra and other data
specs = []
specs_norm = []
zs = []

for spec_file in spec_files:
    spec = []
    with open(spec_file) as f:
        for line in f:
            spec.append(line.split(" ")[1])
    specs.append(spec)

for spec in specs:
    pylab.plot(spec)

pylab.show()
