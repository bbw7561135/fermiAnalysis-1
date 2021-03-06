# N.B Before running, make sure:
#       - all photon files are in a folder called 'photon'
#       - the spacecraft file is named 'spacecraft.fits' and is in a folder called 'spacecraft'
#       You have these 4 files in a folder called model:
#              i) gll_iem_v05.fits
#              ii) gll_iem_v05_rev1.fit
#              iii) gll_psc_v08.fit
#              iv) iso_source_v05_rev1.txt
#              v) iso_clean_v05.txt


import gt_apps as my_apps
import os
bashCommand = "ls -1 ./photon/*.fits > filelist.list"
os.system(bashCommand)
spacecraftFile='./spacecraft/spacecraft.fits'

###############################################
############ Adjustable paramaters ############
###############################################
evClass=2

RA= 193.98
DEC=-5.82
roi=20

eMin=100
eMax=100000
tMin=
tMax=255398400			# 256970880

irfsType='CALDB'       # or 'P7REP_SOURCE_V15' ?
optimizerType = 'NewMinuit'	# or Minuit

createAitoff=0
###############################################

##### Naming stuff #####
file = open('filelist.list', 'r')
name_temp=file.readline()
file.close()
name_type= name_temp[9:12]                                                      # Usually LAT
if (float(eMin/1000.0)).is_integer():                                                      # Usually LAT
	name_energy=str(int(eMin/1000.0))+'-'+str(int(eMax/1000.0))+'GeV' 
else:
	name_energy=str(float(eMin/1000.0)).replace('.', ',')+'-'+str(int(eMax/1000.0))+'GeV'                   # i.e 100Ge

gtselectOutfile=name_type+'_allphotondata_'+name_energy+'.fits'
filteredLATFile = name_type+'_filtered_'+name_energy+'.fits'
gtbinnedFile = name_type+'_binned3600_'+name_energy+'.fits'
ltCubeFile=name_type+'_ltCube_'+name_energy+'.fits'
expMapFile=name_type+'_expMap_'+name_energy+'_'+irfsType+'.fits'
filteredLATFile_withDiffResps = name_type+'_filtered_wDiffResps_'+irfsType+'_'+name_energy+'.fits'

modelFile=name_type+'_'+name_energy+'_model.xml'

########################

###############################################

# Quick check to see if any files already exist
normalFiles_temp=[gtselectOutfile,filteredLATFile,ltCubeFile,expMapFile,modelFile]
binningFiles_temp=[]

normalFiles=[]
binningFiles=[]
for x in normalFiles_temp:
	if os.path.isfile(x):
		normalFiles.append(x)

for y in binningFiles_temp:
	if os.path.isfile(y):
		binningFiles.append(y)

if len(normalFiles)>0 or len(binningFiles)>0:
	print "WARNING: THESE FILES EXIST:"
	if len(normalFiles)>0:
		print '############# Normal Files #############'
		for x in normalFiles:
			print x
	if len(binningFiles)>0:
		print '############# Binning Files #############'
		for x in binningFiles:
			print x
	print 'MAKE SURE YOU ARE USING THE RIGHT ONES/NOT OVERWRITING ANYTHING IMPORTANT!'

	doIContinue = raw_input('Do you want to continue? (y/n):')

	if not (doIContinue=='y' or doIContinue=='Y' or doIContinue=='yes' or doIContinue=='Yes' or doIContinue=='YES'):
		print 'Exiting'
		exit ()
###############################################

def printDictionaryToFile(dictionary,filename):
	fid=open(filename,'w')
	for source,TS in dictionary.iteritems():
		fid.write("%s : %f\n" %(source,TS))
	fid.close()
	os.system('mv '+filename+' results')

# Start analysis

#Run gtselect
my_apps.filter['evclass'] = evClass
my_apps.filter['ra'] = RA
my_apps.filter['dec'] = DEC
my_apps.filter['rad'] = roi
my_apps.filter['emin'] = eMin
my_apps.filter['emax'] = eMax
my_apps.filter['zmax'] = 100
my_apps.filter['tmin'] = 239557417	# This is the earliest Fermi MET
my_apps.filter['tmax'] = tMax
my_apps.filter['infile'] = '@filelist.list'
my_apps.filter['outfile'] = gtselectOutfile
my_apps.filter.run()

#Run gtmktime
my_apps.maketime['scfile'] = spacecraftFile
my_apps.maketime['filter'] = '(DATA_QUAL>0)&&(LAT_CONFIG==1)'
my_apps.maketime['roicut'] = 'yes'
my_apps.maketime['evfile'] = gtselectOutfile
my_apps.maketime['outfile'] = filteredLATFile
my_apps.maketime.run()

my_apps.evtbin['algorithm'] = 'CMAP'
my_apps.evtbin['evfile'] = filteredLATFile
my_apps.evtbin['outfile'] = gtbinnedFile
my_apps.evtbin['scfile'] = spacecraftFile
my_apps.evtbin['nxpix'] = 160
my_apps.evtbin['nypix'] = 160
my_apps.evtbin['binsz'] = 0.25
my_apps.evtbin['coordsys'] = 'CEL'
my_apps.evtbin['xref'] = RA
my_apps.evtbin['yref'] = DEC
my_apps.evtbin['axisrot'] = 0.0
my_apps.evtbin['proj'] = 'AIT'
my_apps.evtbin.run()

# Make an exposure map
my_apps.expMap['evfile'] = filteredLATFile
my_apps.expMap['scfile'] =spacecraftFile
my_apps.expMap['expcube'] =ltCubeFile
my_apps.expMap['outfile'] =expMapFile
my_apps.expMap['irfs'] =irfsType
my_apps.expMap['srcrad'] =min(max(1.5*roi,roi+10),180)    # Source Region should be larger than the Region of Interest by ~50% (or 10 degrees for smaller numbers). BUT NEVER BIGGER THEN 180!
my_apps.expMap['nlong'] =120
my_apps.expMap['nlat'] =120
my_apps.expMap['nenergies'] =20
my_apps.expMap.run()

# Generate XML Model File
from make2FGLxml import *
mymodel = srcList('model/gll_psc_v08.fit',filteredLATFile,modelFile)
mymodel.makeModel('model/gll_iem_v05_rev1.fit', 'gll_iem_v05_rev1', 'model/iso_source_v05_rev1.txt', 'iso_source_v05_rev1')

# There should now be a modelFile with a name SIMILAR to LAT_modelFile.xml

# Run the Diffuse response (Only if you are NOT using CALDB)

# Each event must have a separate response precomputed for each diffuse component in the source model. The precomputed responses for Pass 7 (V6) data are for the gll_iem_v05, iso_source_v05.txt, and iso_clean_05.txt diffuse models.

os.system('cp '+filteredLATFile+' '+filteredLATFile_withDiffResps)	#Make a copy of the filteredLATFile
my_apps.diffResps['evfile']=filteredLATFile_withDiffResps
my_apps.diffResps['scfile']=spacecraftFile
my_apps.diffResps['srcmdl']=modelFile
my_apps.diffResps['irfs']=irfsType
my_apps.diffResps.run()
	

# Run the Likelihood Analysis
import pyLikelihood
from UnbinnedAnalysis import *
obs = UnbinnedObs(filteredLATFile_withDiffResps,spacecraftFile,expMap=expMapFile,expCube=ltCubeFile,irfs=irfsType)
like = UnbinnedAnalysis(obs,modelFile,optimizer=optimizerType)

# Analysis Complete
print "################ Analysis Complete ################"
print obs
print like
print "###################################################"

# Some plots!

like.tol
like.tolType
like.tol = 0.0001
if optimizerType=='Minuit':
	likeobj = pyLike.Minuit(like.logLike)
elif optimizerType=='NewMinuit':
	likeobj = pyLike.NewMinuit(like.logLike)
else:
	print "Error: Bad Optimizer. Exiting"
	exit()
like.fit(verbosity=0,covar=True,optObject=likeobj)                 # Warning: This takes VERY long ~ 1 hour

# Get all the TS values of the sources in the model
sourceDetails = {}
for source in like.sourceNames():
   sourceDetails[source] = like.Ts(source)

# Output for data
os.system('mkdir results')
printDictionaryToFile(sourceDetails,'TSValues_preDelete.txt')

# N.B A source with a TS value less than 0 should never happen unless the minimization failed. Remove that source and try fitting again and check the return code again.
print "Zero?: %d" %(likeobj.getRetCode()) # This value should be zero, refit using the method below if not

# Delete useing like.deleteSource('_2FGLJ1625.2-0020')

# Protip, you can really simplify the model by removing sources with TS levels below 9 (about 3 sigma)
for source,TS in sourceDetails.iteritems():
	print source, TS
	if (TS < 9.0):
		print "Deleting..."
		like.deleteSource(source)
# Refit
like.fit(verbosity=0,covar=True,optObject=likeobj)

print "Zero?: %d" %(likeobj.getRetCode()) 

sourceDetails = {}
for source in like.sourceNames():
   sourceDetails[source] = like.Ts(source)

printDictionaryToFile(sourceDetails,'TSValues.txt')

# Make some plots!

import matplotlib.pyplot as plt
import numpy as np

E = (like.energies[:-1] + like.energies[1:])/2.
# The 'energies' array are the endpoints so we take the midpoint of the bins.

plt.figure(figsize=(9,9))
plt.ylim((0.4,1e4))
plt.xlim((200,300000))
sum_model = np.zeros_like(like._srcCnts(like.sourceNames()[0]))

for sourceName in like.sourceNames():
   sum_model = sum_model + like._srcCnts(sourceName)
   plt.loglog(E,like._srcCnts(sourceName),label=sourceName[1:])

plt.loglog(E,sum_model,label='Total Model')
plt.errorbar(E,like._Nobs(),yerr=np.sqrt(like._Nobs()), fmt='o',label='Counts')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.savefig('results/1.eps',format='eps', bbox_inches='tight')                       # Save figure!


# Plot residuals
sum_counts=sum_model                                        # Is this right? Probably not :/
resid = (like._Nobs() - sum_counts)/sum_counts
resid_err = (np.sqrt(like._Nobs())/sum_counts)
plt.figure(figsize=(9,9))
plt.xscale('log')
plt.errorbar(E,resid,yerr=resid_err,fmt='o')
plt.axhline(0.0,ls=':')
plt.savefig('results/2.eps',format='eps', bbox_inches='tight')

# Get indexes and stuff
fid=open('results/'+name_type+'_results.txt','w')
for sourceName in like.sourceNames():
	fid.write(str(like.model[sourceName]))
	fid.write('Flux: '+str(like.flux(sourceName,emin=eMin))+'\n')
	fid.write('Flux Error: '+str(like.fluxError(sourceName,emin=eMin))+'\n')
	fid.write('TS: '+str(like.Ts(sourceName))+'\n')
	fid.write('Sigma: '+str(np.sqrt(like.Ts(sourceName)))+'\n')
	fid.write('\n=====================================\n')
fid.close()

# Save .xml
like.logLike.writeXml('results/'+name_type+'_results.xml')

