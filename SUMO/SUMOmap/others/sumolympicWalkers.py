#!/usr/bin/python
#parameters

outfile="sumolympicWalkers.rou.xml"
startEdge="beg"
endEdge="end"
departTime=0 #time of depart
departPos=-30. #position of depart
arrivalPos= 100. #position of arrival
numberTrips= 100

#generate XML
xml_string="<routes>\n"
for i in range(numberTrips):
	#xml_string +='   <person depart="%f" id="p%d" departPos="last" >\n' % (departTime, i, departPos)
	xml_string +='    <person depart="%f" id="p%d" departPos="+50.0" >\n' % (departTime, i)
	xml_string +='       <walk edges="%s %s" arrivalPos="%f" /> \n' % (startEdge, endEdge, arrivalPos)
	xml_string +='	 </person>\n'

xml_string+="</routes>\n"

with open(outfile,"w") as f:
	f.write(xml_string)

f.close()

