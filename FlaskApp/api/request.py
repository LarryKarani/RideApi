from datetime import datetime

from .rideoffers import RideOffer






class RequestsJ():
    #stores  all the request
    ride_request= []

    def __init__(self, name, From, To, seats_needed, time, rideId):
        self.name = name
        self.From = From
        self.To = To
        self.seats_needed = seats_needed
        self.time = time
        self.rideId = rideId
    
    def request_ride(self):
        #creates a request and adds it to the list of ride_request 
        self.date_requested = str(datetime.now())
        self.id = 1

        if len(self.ride_request) != 0:
            self.id = len(self.ride_request) + 1
        
        self.ride_request={
            'id': self.id,
             'requester': self.name,
             'From': self.From,
             'To':self.To,
             'seats_needed':self.seats_needed,
             'time':self.time,
             'date_requested':self.date_requested,
            
        }

        return self.ride_request