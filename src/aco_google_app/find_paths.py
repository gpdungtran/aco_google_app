import googlemaps
from datetime import datetime
from ant_colony import AntColony
import json
import numpy as np
gmaps = googlemaps.Client(key='AIzaSyBnEczbljpLOsESpId-YPwFWQNc4YuYLEk')

# Request directions via public transit
now = datetime.now()

def path_obtain(places,traffic_mode = "walking"):
    origins = places
    destinations = places
    print(places)
    distance_matrix_result = gmaps.distance_matrix(origins, destinations, mode=traffic_mode, language=None, avoid=None, units=None, departure_time=None, 
    arrival_time=None, transit_mode=None, transit_routing_preference=None, traffic_model=None, region=None)

    #Obtain distance matrix
    distance_list = []
    
    for items in distance_matrix_result["rows"]:
        for item in items["elements"]:
            if 'distance' in item.keys():
                distance_list.append(item["distance"]["value"])
            else:
                distance_list.append(0)
               
    distance_list = [np.inf if item == 0 else item for item in distance_list]
       
    distance_matrix = np.array(distance_list)

    distance_matrix = distance_matrix.reshape(len(origins),len(origins))
    

    #Apply Ant conoly optimization
    ant_colony = AntColony(distance_matrix, 10, 10, 100, 0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()
    print ("shorted_path: {}".format(shortest_path))
    
    path_name = []
    res =[]
    for item in shortest_path[0]:
    
        start_path = origins[int(item[0])]
        end_path = origins[int(item[1])]
        path_name.append((start_path,end_path))
        directions_result = gmaps.directions(start_path,end_path,mode=traffic_mode,departure_time=now)
        res_add = [val["points"] for key, val in directions_result[0].items() if "points" in val]
        res.append(res_add[0])
    
    return res,path_name

