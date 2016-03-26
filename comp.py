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
spec_files = sys.argv[1:]

#Holder for composite spectra and other data
specs = []

for spec_file in spec_files:
    spec = []
    with open(spec_file) as f: #Grab the file...
        for line in f: #Line by line...
            spec.append(line.split(" ")) #Split it up..
    spec = list(map(list, zip(*spec))) #And then transpose it
    specs.append(spec)

#Generate the average(s)
specs_sum = np.zeros(1760)
specs_sum_squares = np.zeros(1760)
for spec in specs:
    for i in range(len(spec[1])):
        specs_sum[i] += float(spec[1][i])
        specs_sum_squares[i] += float(spec[1][i])**2

specs_mean = specs_sum / len(specs)
specs_mean_squares = specs_sum_squares / len(specs)

sigma = np.sqrt(specs_mean_squares - specs_mean**2)

#Make something pretty!
#for spec in specs:
#    pylab.plot(spec[1])

pylab.plot(specs_mean)

pylab.show()
