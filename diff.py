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
comp = fits.open(comp_file)
spec_comp = comp[1].data

#Holder for composite spectra and other data
specs = []
specs_diff = []
zs = []

for spec_file in spec_files:
    #Read in spectral data
    hdulist = fits.open(spec_file)

    #Extract spectra
    spec = list(hdulist[1].data['flux'])

    #Add z shift to list
    #zs.append(hdulist[2].data['Z'])

    #Calculate deltas...
    min_entries = max(map(len, [spec, spec_comp['spec_comp_raw']]))
    spec_diff = spec - list(spec_comp)[0:min_entries]

    #Add to specra list... for later use...
    specs.append(spec)
    specs_diff.append(spec_diff)

    #GC by hand.. damn snake
    del spec
    hdulist.close()

#pylab.plot(spec_comp['sigma_max_norm'], color="black")
#pylab.plot(spec_comp['spec_comp_norm'], color="black")
#pylab.plot(spec_comp['sigma_min_norm'], color="black")
pylab.plot(spec_comp['spec_comp_raw'])
pylab.plot(specs[2])
pylab.show()
