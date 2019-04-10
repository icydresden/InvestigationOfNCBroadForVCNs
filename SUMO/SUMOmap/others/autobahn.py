#!/usr/bin/python
#parameters
from enum inport Enum,unique

outfile="autobahn.rou.xml"
numberFlow=4 # number of flows

@unique
class vClass(Enum):
	car="passenger"
	trailer="trailer"
	coach="coach"

xml_string='<routes>\n'

for in in range(numberFlow):
	pass

with open(outfile,'w') as f:
	f.write(xml_string)

f.close()
