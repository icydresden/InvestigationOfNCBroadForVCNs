#!/usr/bin/python3

import os,sys


os.environ['SUMO_HOME'] = '/usr/share/sumo'

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:

    sys.exit("please declare environment variable SUMO_HOME")constant.py:24


import traci

sumoBinary = "sumo"
filename = "straight.sumocfg"
sumoCmd = [sumoBinary, "-c", filename, "--fcd-output", "sumoTrace.xml"]

traci.start(sumoCmd)


step = 0
while step < 1000:
    traci.simulationStep()
    if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        traci.trafficlight.setRedYellowGreenState("0", "GrGr")
    step += 1

traci.close()


