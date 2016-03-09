from os import listdir
from os.path import isfile, join
from astropy.io import fits
from scipy.interpolate import interp1d

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
spec_files = glob.glob('data/*.fits')

#Holder for composite spectra and other data
specs = []
specs_norm = []
zs = []

for spec_file in spec_files:
    #Read in spectral data
    hdulist = fits.open(spec_file)

    #Extract spectra
    spec = hdulist[1].data['flux']

    #Add z shift to list
    zs.append(hdulist[2].data['Z'])

    #Add to specra list... for later use...
    specs.append(spec)

max_entries = max(map(len, specs))

#Average composite... probably a better way...
spec_sum = np.zeros(max_entries)
for spec in specs:
    for i in range(len(spec) - 1):
        spec_sum[i] += spec[i]

spec_comp = spec_sum / len(specs)

#Run moving average on composite
#spec_comp_smooth = movingaverage(spec_comp, 50)
#spec_comp_norm = spec_comp * 1/max(spec_comp)

#Get <x^2>
spec_sum_squares = np.zeros(max_entries)
for spec in specs:
    for i in range(len(spec) - 1):
        spec_sum_squares[i] += spec[i]**2

spec_mean_squares = spec_sum_squares / len(specs)

#Calculate Sigmas
sigma = spec_mean_squares - spec_comp**2
spec_sigma_max = spec_comp + sigma
spec_sigma_min = spec_comp - sigma

#Lets plot something.. just for looks
#pylab.plot(normalize(spec_sigma_max), color="blue")
#pylab.plot(normalize(spec_sigma_min), color="green")
pylab.plot(normalize(spec_comp), color="red")
pylab.plot(normalize(sigma))

pylab.title('QSO Comp Spectra')
pylab.text(50, 0.1, 'z :~' + str(np.min(zs)) + " - " + str(np.max(zs)))
pylab.show()
