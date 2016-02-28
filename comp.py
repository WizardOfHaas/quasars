from os import listdir
from os.path import isfile, join
from astropy.io import fits

import numpy as np
import pylab

#List of spectra to read...
spec_files = [f for f in listdir('data/') if isfile(join('data/', f))]

#Holder for composite spectra
specs = []

for spec_file in spec_files:
	#Read in spectral data
	hdulist = fits.open('data/' + spec_file)
	spec = hdulist[0].data[1]

	#Normalize
	spec_max = max(spec)
	spec_norm = [x / spec_max for x in spec]

	#Add to specra list... for later use...
	specs.append(spec_norm)

	#Hows it lookin?
	#pylab.plot(spec_norm)

#Build composite.. probably a better way...
spec_sum = np.zeros(len(specs[0]) + 10)
for spec in specs:
	for i in range(len(spec) - 1):
		spec_sum[i] += spec[i]

spec_comp = map(lambda x: x / (len(specs)), spec_sum)

pylab.plot(spec_comp)
pylab.show()