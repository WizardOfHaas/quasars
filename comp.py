from os import listdir
from os.path import isfile, join
from astropy.io import fits
from scipy.interpolate import interp1d

import numpy as np
import pylab

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

#List of spectra to read...
spec_files = [f for f in listdir('data/') if isfile(join('data/', f))]

#Holder for composite spectra and other data
specs = []
zs = []

for spec_file in spec_files:
	#Read in spectral data
	hdulist = fits.open('data/' + spec_file)
	spec = hdulist[0].data[1]
	zs.append(hdulist[0].header['z'])

	#Normalize
	spec_max = max(spec)
	spec_norm = [x / spec_max for x in spec]

	#Add to specra list... for later use...
	specs.append(spec_norm)

	#Hows it lookin?
	#pylab.plot(spec_norm)

#Average composite.. probably a better way...
spec_sum = np.zeros(len(specs[0]) + 100)
for spec in specs:
	for i in range(len(spec) - 1):
		spec_sum[i] += spec[i]

spec_comp = map(lambda x: x / (len(specs)), spec_sum)

#Run moving average on composite
spec_comp_smooth = movingaverage(spec_comp, 50)

pylab.plot(spec_comp_smooth, color="red")
pylab.title('QSO Comp Spectra')
pylab.text(50, 0.1, 'z :~' + str(np.min(zs)) + " - " + str(np.max(zs)))
pylab.show()
