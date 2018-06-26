from datetime import datetime

from .rideoffers import RideOffer
from.user import User


rideoffer = RideOffer()


class RequestsJ:
    #stores  all the request
    ride_request= []
    
    def request_ride(self, name, From, To, seats_needed, time,rideId):
        #creates a request and adds it to the list of ride_request 
        self.date_requested = str(datetime.now())
        
        
        self.id = 1

        if len(self.ride_request) != 0:
            self.id = len(self.ride_request) + 1
        
        self.ride_request={
            'id': self.id,
             'requester': name,
             'From': From,
             'To':To,
             'seats_needed':seats_needed,
             'time':time,
            
             'date_requested':self.date_requested
        }

        return self.ride_request