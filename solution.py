'''
solution.py
:desc: This script return a list of fligths in json format with detailed information about flights available.
you should provide origin, destination, number of bags and if is a return flight.
__author__:Hector Navarro-Barboza
'''
import argparse
from csv import DictReader
import json
from datetime import datetime


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
            return flights
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
                        
                    else:
                        pass
                route.append(routes)
                print(json.dumps(route))
                return json.dumps(route)

            else:
                avail_flights = []
                for i, flight in enumerate(self.read_data()):
                    if flight["origin"] == self.origin and int(flight["bags_allowed"]) >= self.bags and flight['destination']==self.destination:
                        avail_flights.append(self.read_data()[i])
                new=[]
                flight_ = {"flights":{}}
                for f in avail_flights:
                    flight_['flights'] = f
                    flight_["bags_allowed"] = int(f["bags_allowed"])
                    flight_["bags_count"] = self.bags
                    flight_["destination"] = self.destination
                    flight_["origin"] = self.origin
                    flight_["total_price"] = float(f["base_price"]) + int(f["bag_price"])*self.bags
                    flight_["travel_time"] = str(datetime.fromisoformat(f["arrival"]) - datetime.fromisoformat(f["departure"]))
                new.append(flight_)
                print(json.dumps(new))
            return json.dumps(new)
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
    flights.find_route()
