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
comp_file = sys.argv[1]
spec_files = sys.argv[2:-1]

#Read in composite...
spec_comp = fits.open(comp_file)

#Holder for composite spectra and other data
specs = []
specs_norm = []
zs = []

for spec_file in spec_files:
    #Read in spectral data
    hdulist = fits.open(spec_file)

    #Extract spectra
    spec = list(hdulist[1].data['flux'])

    #Add z shift to list
    #zs.append(hdulist[2].data['Z'])

    #Add to specra list... for later use...
    specs.append(spec)

    #GC by hand.. damn snake
    del spec
    hdulist.close()
