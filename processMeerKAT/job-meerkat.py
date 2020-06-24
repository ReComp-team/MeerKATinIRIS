#!/usr/bin/env python
#
# Template for submitting lots of jobs to GridPP DIRAC or LHCb DIRAC
# Lots of inline comments. Please edit to suit your situation.
#
# This script uses DIRAC parametric jobs:
#  https://github.com/DIRACGrid/DIRAC/wiki/JobManagementAdvanced

import sys
import time

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.Interfaces.API.Dirac import Dirac

# We construct the DIRAC Job Description Language as string in jdl:
jdl = ''

# Something descriptive for the name! Like 'RunMeerKAT'.
jdl += 'JobName = "RunMeerKAT";\n'
#jdl +=  'Parameters = "LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/1491550051.tar.gz";\n'
jdl += 'Tags = {"skatelescope.eu.hmem","8Processors"};\n'
jdl += 'Platform = "EL7";\n'

jdl += 'Site = "LCG.UKI-NORTHGRID-MAN-HEP.uk";\n'
#jdl += 'SmpGranularity = 6;\n'
#jdl += 'CPUNumber = 6;\n'
jdl += 'OutputSE = "UKI-NORTHGRID-MAN-HEP-disk";\n'
#if len(sys.argv) > 1:
# timeSamples = sys.argv[1]
#else:
# timeSamples = ''

# The script you want to run. 
jdl += 'Executable = "run-meerkat-on-iris.sh";\n'

# tarJob.sh will be run with these command line arguments
# %n is a counter increasing by one for each job in the list
# %s is the parameter taken from the list given in Parameters = { ... }
# %j is the unique DIRAC Job ID number
# something is just a value to show you can add other things too
jdl += 'Arguments = "%j %n %s";\n'

# Send the script you want to run (in this directory where you run man-job-submit
# or give the full path to it)
jdl += 'InputSandbox = {"run-meerkat-on-iris.sh","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/cal_scripts.tar.gz","myconfig.txt","config_parser.py","processMeerKAT.py","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/casameer-5.4.1.xvfb.simg","prmon_1.0.1_x86_64-static-gnu72-opt.tar.gz","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT_DataSets/1491550051.ms.tar.gz"};\n'
# Tell DIRAC where to get your big input data files from
# %s is the parameter taken from the list given in Parameters = { ... }
jdl += 'InputData = {"LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT_DataSets/1491550051.ms.tar.gz"};\n'
                      
# Direct stdout and stderr to files
jdl += 'StdOutput = "StdOut";\n'
jdl += 'StdError = "StdErr";\n'

# Small files can be put in the output sandbox
jdl += 'OutputSandbox = {"StdOut", "StdErr"};\n'

# Files to be saved to your grid storage area in case they are large
# %j is the unique DIRAC Job ID number. 
# DIRAC looks for this output file in the working directory.
jdl += 'OutputData = {"LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/outputMMS_%j.tar.gz","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/prmon_validate_partition_%j.txt","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/myconfig_%j.txt","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/images_%j.tar.gz","LFN:/skatelescope.eu/user/p/priyaa.thavasimani/MeerKAT/plots_%j.tar.gz"};\n'

# Give the OutputSE too if using OutputData:
jdl += 'OutputSE = "UKI-NORTHGRID-MAN-HEP-disk";\n'	# storage in GridPP DIRAC
# jdl += 'OutputSE = "CERN-USER";\n'			# storage in LHCb DIRAC

# Tell DIRAC how many seconds your job might run for 
# jdl += 'MaxCPUTime = 1000;\n'

# Create a unique Job Group for this set of jobs
try:
  diracUsername = getProxyInfo()['Value']['username']
except:
  print 'Failed to get DIRAC username. No proxy set up?'
  sys.exit(1)

jobGroup = 'running meerkat 8 processors' 
jdl += 'JobGroup = "' + jobGroup + '";\n'

print 'Will submit this DIRAC JDL:'
print '====='
print jdl
print '====='
print
# Submit the job(s)
print 'Attempting to submit job(s) in JobGroup ' + jobGroup
print
dirac = Dirac()
result = dirac.submitJob(jdl)
print
print '====='
print
print 'Submission Result: ',result
print
print '====='
print

if result['OK']:
  print 'Retrieve output with  dirac-wms-job-get-output --JobGroup ' + jobGroup
else:
  print 'There was a problem submitting your job(s) - see above!!!'
print
