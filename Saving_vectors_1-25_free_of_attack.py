import os, sys
import subprocess
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import Estimator as estimator
import TrafficRouter as router
import Sensors as sensors
#import ReportGenerator as report
import Map
import sys
import time
start_time = time.time()
print 'Executing python code ...'
print("--- %s seconds ---" % (time.time() - start_time))
####### ADD "sumo-tools" (and TraCI) to the path
tools_path                      = '../sumo-0.26.0-tools'
sys.path.append(tools_path)
import traci
import csv

####### GUI Options
USE_GUI                         = 1   # 0 = no GUI, 1 = open GUI

####### GLOBAL VARIABLES  #######
PORT                            = 8813
EXAMPLE_FILE                    = "../new_bolo/bolognaringway.sumo.cfg"
SIMULATIN_STEP_COUNT            = 1     # controls how many simulation steps we skip before reourting
USE_GROUNDTRUTH                 = 0    # <only for routing> used to switch between secure routing (0) and ground truth routing (1)
USE_NOISY                       = 1     # used to choose between noisy (1) and non-noisy (0) measurements
noise_sigma                     = 3  # variance of noise added to velocities
MAX_SIMULATION_STEPS            = 3600  # simulation length
USE_SYBIL                       = 1 # 1 for sybil, 0 for 
USE_ROBUST_ESTIMATOR            = 1 # 0 for non robust estimation, 1 for robust (SMT chain)
#attackType                      = 'congest_sideway'
attackType                      = 'congest_highway'
num_Sybil                       = 0 # number of sybil cars inserted by a dishonest car

deviation                       = 0#int(sys.argv[1])
loop_noise_sigma                = 10#float(sys.argv[2])
#depart_time                     = int(sys.argv[3])

print 'deviation (from Python code):', deviation
print 'sigma of noise (from Python code) added in estimator for actual velo: ', loop_noise_sigma
# for now, for sybil use SYBIL = 0, for ground truth use 

# need to clean the options... sybil, use_noisy and use_groundtruth

def get_all_edges(route_list) :
    # finds all of the edges for the routes, returns a list of edges here
    # in order to be more efficient when checking, converting the list into a set
    edgeIDs = set()
    for route in route_list :
        for edge in traci.route.getEdges(route) :
            if edge not in edgeIDs :
                edgeIDs.add(edge)
    return edgeIDs

def getMeasurements(minute) :
    csv_file = file ("./output/edgeMeasurements_free_of_attack.csv","r")
    reader = csv.reader(csv_file)
    edgeMeasurements = []
    for line in reader :
        if minute == int(line[0]) :
            edgeMeasurements = eval(line[1])
    csv_file.close()

    #print edgeMeasurements

    return edgeMeasurements

####### EXECUTE TraCI CONTROL LOOP #######
def run():
    traci.init(PORT)
    step                                = 0
    simCount                            = 0
    
    numOfEdges                          = traci.edge.getIDCount()

    # in the initial bologna scenario, we have only 2 routes
    route_list                          = ["route1","route2"]
    edgeIDs                             = get_all_edges(route_list)
    attacked_edges_list                 = ['151772103#1', '151772103#0', '34547773', '150018080#0', '151737991#0', '293300505#4', '151824722#2', '151824722#3', '151737996', '-43469287#3', '150018085#0', '151737991#2' ]
    print "num of attacked edges:",len(attacked_edges_list)
    calculatedTravelEstimate_history    = list()
    
    calculatedTravelEstimate_history.append(Map.Map(routeId = "route1", travelTime = list()))
    calculatedTravelEstimate_history.append(Map.Map(routeId = "route2", travelTime = list()))

    #create a csv file for saving edgeMeasurements without attack for the first 25mins
    csv_file = file ("./output/edgeMeasurements_free_of_attack.csv","r")
    reader=csv.reader(csv_file)
    #writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
    
    while traci.simulation.getMinExpectedNumber() > 0 and simCount < MAX_SIMULATION_STEPS :
        # SIMULATE THE SYSTEM
        step                    = step + 1
        simCount                = simCount + 1
        traci.simulationStep()
    
        if step < SIMULATIN_STEP_COUNT:
            continue
        else:
            step = 0

        # returning the measurements for each edge
        #measurements             = sensors.generateDishonestSybilSensorMeasurements(attackType, deviation, num_Sybil, attacked_edges_list, edgeIDs, 0.2)
       
        # print len(measurements)
        # saving the edgeMeasurements for routes in route_list
        #if simCount % 60 == 0:
            #every minute
            #writer.writerow([str(simCount/60),str(measurements)])

        # update the travel time for each edge, and then add them up, returning a list of travel time for each route
        # parameters:(measurements, USE_ROBUST_ESTIMATOR, loop_noise_sigma, route_list)
        if simCount == 1500 :
            #print "getMeasurements(2),",getMeasurements(2)
            travelTimeEstimate      = estimator.updateEstimate(getMeasurements(25), USE_ROBUST_ESTIMATOR, loop_noise_sigma, route_list)
            print "120s",travelTimeEstimate[0],travelTimeEstimate[1]
            calculatedTravelEstimate_history[0].travelTime.append(travelTimeEstimate[0].travelTime)
            calculatedTravelEstimate_history[1].travelTime.append(travelTimeEstimate[1].travelTime)
        

    #csv_file.close()
    traci.close()
    sys.stdout.flush()


    

####### MAIN ENTRY #######
if __name__ == "__main__":
    if(USE_GUI == 0):
        sumoBinary                  = "sumo"
    else:
        sumoBinary                  = "sumo-gui"
    out_file                    = "./output-no-depart.xml"
    sumoProcess                 = subprocess.Popen([sumoBinary, "-c", EXAMPLE_FILE, "--remote-port", str(PORT), '--tripinfo-output', out_file ], stdout=sys.stdout, stderr=sys.stderr)
    #print "---output tripinfo--:output-depart-"+str(depart_time)+".xml"
    run()
    sumoProcess.wait()
    print 'End'
    print("--- %s seconds ---" % (time.time() - start_time))