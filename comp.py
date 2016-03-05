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
    spec_smooth = movingaverage(spec_norm, 3)
    spec_smooth = spec_smooth * 1/max(spec_smooth)
    specs_norm.append(spec_smooth.tolist())

#Average composite.. probably a better way...
spec_sum = np.zeros(len(specs[0]) + 100)
for spec in specs:
    for i in range(len(spec) - 1):
        spec_sum[i] += spec[i]

spec_comp = map(lambda x: x / (len(specs)), spec_sum)

#Run moving average on composite
spec_comp_smooth = movingaverage(spec_comp, 50)
spec_comp_norm = spec_comp_smooth * 1/max(spec_comp_smooth)

#Generate Max/Min Spectra
spec_max = np.amax(specs_norm, axis=0)
spec_min = np.amin(specs_norm, axis=0)

#Lets plot something.. just for looks
pylab.plot(spec_min, color="green")
pylab.plot(spec_max, color="blue")
pylab.plot(spec_comp_norm, color="red")

pylab.title('QSO Comp Spectra')
pylab.text(50, 0.1, 'z :~' + str(np.min(zs)) + " - " + str(np.max(zs)))
pylab.show()
 
 #hello friend
 
