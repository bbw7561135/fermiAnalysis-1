evClass=3
spacecraftFilter='(DATA_QUAL>0)&&(LAT_CONFIG==1)&&ABS(ROCK_ANGLE)<52'

RA= 90.065700
DEC=12.761580
ROI=5

TSThreshold=9.0

eMin=100000
eMax=500000
tMin=239557417				# This is the earliest Fermi MET
tMax='INDEF'			# 256970880

irfsType='P7REP_SOURCE_V15'       # or 'P7REP_SOURCE_V15' ?
optimizerType = 'NewMinuit'	# or Minuit

createAitoff=0
mySources=True
