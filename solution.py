'''
solution.py
:desc: This script return a list of fligths in json format with detailed information about flights available.
you should provide origin, destination, number of bags and if is a return flight.
__author__:Hector Navarro-Barboza
'''
import argparse
from csv import DictReader
import json
from datetime import datetime, timedelta


class SearchFlight:
    def __init__(self, file, origin, destination, bags, return_):
        self.file = file
        self.origin = origin
        self.destination = destination
        self.bags = bags
        self.return_ = return_
    
    def read_data(self):
        '''
        Return a dictionary with data available according to 
        file given.
        '''
        try:
            flights = []
            with open(self.file) as f:
                reader = DictReader(f)
                for flight in reader:
                    flights.append(flight)
            data = flights.copy()
            for f in data:
                if int(f['bags_allowed']) < self.bags:
                    data.remove(f)
            return data
        except:
            print('Data path is not valid or doesnt exist')

    def is_valid(self):
        '''
        Return a message if origin or destination are not in data provided
        '''
        try:
            origins = []
            destinations = []
            for origin in self.read_data():
                origins.append(origin['origin'])
            for destination in self.read_data():
                destinations.append(destination['destination'])
            if (self.origin not in origins) or (self.destination not in destinations):
                return print(f'Your origin fligth {self.origin} or destination {self.destination} is not in data')
        except:
            print('Data path is not valid or doesnt exist')
    
    def layover_request(self, arrival_time, departure_time):
        '''
        Return True/False if layover is achieved
        :arrival_time: dictionary of dates
        :departure_time: dictionary of dates
        '''
        req_l = timedelta(hours=1) <= datetime.fromisoformat(departure_time["departure"]) -\
                        datetime.fromisoformat(arrival_time["arrival"]) <= timedelta(hours=6)
        return req_l


    def flights_connected(self, trips, data):
        con_list = []
        for x in data:
            if x['origin'] == trips[len(trips) - 1]['destination']:
                if self.layover_request(trips[len(trips) - 1], x):
                    check = True
                    for y in trips:                            # no repeating airports
                        if x['destination'] == y['origin']:
                            check = False
                            break
                    if check:
                        con_list.append(x)
 
        return con_list

    def one_way_flights(self):
        direct_flights = []
        flights_w_conection = []
        for i in self.read_data():
            if i['origin'] == self.origin:
                if i['destination'] == self.destination:
                    direct_flights.append([i])
                else:
                    flights_w_conection.append([i])


        i = 0
        while flights_w_conection:
            departure_list = self.flights_connected(flights_w_conection[i], self.read_data())
            if not departure_list:
                flights_w_conection.pop(i)
            else:
                for j in departure_list:
                    if j['destination'] == self.destination:
                        direct_flights.append([*flights_w_conection[i], j])
                    else:
                        flights_w_conection.append([*flights_w_conection[i], j])
                flights_w_conection.pop(i)

        
        return direct_flights

    def find_route(self):
        try:
            self.is_valid()
            if self.return_:
                orgs =[]
                #First fligths 
                for i, flight in enumerate(self.read_data()):
                    if flight["origin"] == self.origin and int(flight["bags_allowed"]) >= self.bags:
                        orgs.append(self.read_data()[i])
                #second flights
                back = []
                for i, back_flight in enumerate(self.read_data()):
                    #saving destination different 
                    if back_flight['destination'] == self.origin and int(back_flight["bags_allowed"]) >=self.bags:
                        back.append(back_flight)
                #get flights with layover
                route = []
                routes = {}
                flight_go = {"flights": {}}
                flight_back = {"flights": {}}
                for i, j in zip(orgs, back):
                    if j["destination"] == self.origin and i["destination"] == self.destination and i['origin']== self.origin:
                        flight_go["flights"]= i
                        flight_go["bags_allowed"] = int(i["bags_allowed"])
                        flight_go["bags_count"] = self.bags
                        flight_go["destination"] = self.destination
                        flight_go["origin"] = self.origin
                        flight_go["total_price"] = float(i["base_price"]) + int(i["bag_price"])*self.bags
                        flight_go["travel_time"] = str(datetime.fromisoformat(i["arrival"]) - datetime.fromisoformat(i["departure"]))

                        flight_back["flights"]=j
                        flight_back["bags_allowed"] = int(j["bags_allowed"])
                        flight_back["bags_count"] = self.bags
                        flight_back["destination"] = self.destination
                        flight_back["origin"] = self.origin
                        flight_back["total_price"] = float(i["base_price"]) + int(j["bag_price"])*self.bags
                        flight_back["travel_time"] = str(datetime.fromisoformat(j["arrival"]) - datetime.fromisoformat(j["departure"]))
                        routes['go'] = flight_go
                        routes['back'] = flight_back
                        route.append(routes)
                        
                    else:
                        pass
                
                print(json.dumps(route, indent=4))
                return json.dumps(route, indent=4)

            else:
                fly = self.one_way_flights()
                complete_fligths = []          
                for i,f in enumerate(fly):
                    tot_price = 0
                    tot_travel_time = timedelta(hours=0,minutes=0,seconds=0)
                    for j in f:
                        tot_price += float(j['base_price']) + float(j['bag_price'])*self.bags
                        tot_travel_time += datetime.fromisoformat(j["arrival"]) - datetime.fromisoformat(j["departure"])
                    flights_found ={
                        'flights': f,
                        'origin': self.origin,
                        'destination': self.destination,
                        'bags_allowed': f[0]['bags_allowed'],
                        'bags_count': self.bags,
                        'total_price': tot_price,
                        'travel_time': str(tot_travel_time)
                    }
                    complete_fligths.append(flights_found)
                print(json.dumps(complete_fligths, indent=4))
            return json.dumps(complete_fligths, indent=4)
        except:
            print('Data path is not valid or doesnt exist')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_file", type=str)
    parser.add_argument("origin", type=str)
    parser.add_argument("destination", type=str)
    parser.add_argument("-b", "--bags", help="Number of requested bags",\
                        default=0, type=int)
    parser.add_argument("-r", "--return", help="Is it a return flight?",\
                        default=False, type=bool)
    # Reading arguments 
    input_args = vars(parser.parse_args())
    
    flights = SearchFlight(input_args['path_to_file'],\
                           input_args['origin'],\
                           input_args['destination'],\
                           input_args['bags'],\
                           input_args['return'])
    #flights.find_route()
    flights.find_route()