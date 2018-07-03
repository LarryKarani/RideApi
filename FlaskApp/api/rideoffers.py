from datetime import datetime



class RideOffer():
    #holds all ride offers
    ride_offers = []

    def __init__(self, name, From, To, car_model, cost, seats_available, time):
        self.name = name
        self.From = From
        self.To = To
        self.car_model = car_model
        self.cost = cost
        self.seats_available =seats_available
        self.time = time

    def create_ride(self):
        self.id = 1
        self.date_created = str(datetime.now())

        if len(self.ride_offers) != 0:
            self.id = len(self.ride_offers) + 1

        self.ride_offer_dict = {
            'id':self.id,
            'name':self.name,
            'From':self.From,
            'To':self.To,
            'car_model':self.car_model,
            'cost':self.cost,
            'seats_available':self.seats_available,
            'time': self.time,
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