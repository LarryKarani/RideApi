from datetime import datetime
from .user import User


class RideOffer():
    #holds all ride offers
    ride_offers = [{
            'id':1,
            'name':'na',
            'from':'Fom',
            'To':'To',
            'car_model':'car_model',
            'cost':'cost',
            'seats_available':'seats_available',
            'time': 'time'
        }]

    def create_ride(self, name, From, To, car_model, cost, seats_available, time):
        self.id = 1
        #self.user = User.return_user(name)
        """self.user_info = {
                        'name': self.user['username'],
                        'username': self.user['username'],
                        'since': self.user['date_registered']
                         }"""

        self.date_created = str(datetime.now())

        if len(self.ride_offers) != 0:
            self.id = len(self.ride_offers) + 1

        self.ride_offer_dict = {
            'id':self.id,
            'name':name,
            'From':From,
            'To':To,
            'car_model':car_model,
            'cost':cost,
            'seats_available':seats_available,
            'time': time,
            'date_created':self.date_created
        }

        self.ride_offers.append(self.ride_offer_dict)

        return self.ride_offer_dict

    
    
    @staticmethod
    def get_all_rides():
        return RideOffer.ride_offers

    @staticmethod
    def get_specific_offer(id):
        for ride_offer in RideOffer.ride_offers:
            if str(ride_offer['id']) == str(id):
                return ride_offer
            else:
                return{"message": " rideoffer does not exit"}
    


