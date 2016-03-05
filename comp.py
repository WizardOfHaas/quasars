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

#List of spectra to read...
spec_files = glob.glob('data/*.fit')

#Holder for composite spectra and other data
specs = []
specs_norm = []
zs = []

for spec_file in spec_files:
    #Read in spectral data
    hdulist = fits.open(spec_file)
    spec = hdulist[0].data[1]
    zs.append(hdulist[0].header['z'])

    #Normalize
    spec_max = max(spec)
    spec_norm = [x / spec_max for x in spec]

    #Add to specra list... for later use...
    specs.append(spec_norm)

    #Apply moveing average and add to list... for later use...
    spec_smooth = movingaverage(spec_norm, 50)
    spec_smooth = spec_smooth * 1/max(spec_smooth)
    specs_norm.append(spec_smooth.tolist())

#Average composite... probably a better way...
spec_sum = np.zeros(len(specs[0]) + 100)
for spec in specs:
    for i in range(len(spec) - 1):
        spec_sum[i] += spec[i]

spec_comp = spec_sum / len(specs)

#Run moving average on composite
spec_comp_smooth = movingaverage(spec_comp, 50)
spec_comp_norm = spec_comp * 1/max(spec_comp)

#Get <x^2>
spec_sum_squares = np.zeros(len(specs[0]) + 100)
for spec in specs:
    for i in range(len(spec) - 1):
        spec_sum_squares[i] += spec[i]**2

spec_mean_squares = spec_sum_squares / len(specs)
spec_mean_squares_norm = spec_mean_squares * 1/max(spec_mean_squares)

#Calculate Sigmas
spec_sigma_max = spec_comp_norm + spec_mean_squares_norm
spec_sigma_min = spec_comp_norm - spec_mean_squares_norm

#Lets plot something.. just for looks
pylab.plot(spec_sigma_max, color="blue")
pylab.plot(spec_sigma_min, color="green")
pylab.plot(spec_comp_norm, color="red")

pylab.title('QSO Comp Spectra')
pylab.text(50, 0.1, 'z :~' + str(np.min(zs)) + " - " + str(np.max(zs)))
pylab.show()
 
 #hello friend
 #we meet again..
 
