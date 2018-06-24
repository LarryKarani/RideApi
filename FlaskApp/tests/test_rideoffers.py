import unittest
from FlaskApp.api.rideoffers import RideOffer

class RideOfferTestCase(unittest.TestCase):
    def setUp(self):
        self.rideoffer = RideOffer()
    

    def test_create_ride_offer(self):
        self.response = self.rideoffer.create_ride(
            'larry', 'mombasa', 'kirinyaga', '10:30', 
            '29/10/2018', '$80/km', 'Thika road', '5',
            'Toyota'
        )
        self.assertIn(self.response, self.rideoffer.ride_offers)

    def test_get_a_ride_offer(self):
        self.response_in = self.rideoffer.create_ride(
            'larry', 'Tanzania', 'wakanda', '10:30', 
            '29/10/2018', '$80/km', 'Thika road', '5',
            'Toyota'
        )
        self.response_out = self.rideoffer.get_ride_offer(self.response_in['id'])
        self.assertIn(self.response_out, self.rideoffer.ride_offers)
    
    def test_get_all_ride_offers(self):
        self.response = self.rideoffer.get_all_rides()
        self.assertTrue(len(self.response)==len(self.rideoffer.ride_offers))
         
    def test_request_to_join(self):
        self.response = self.ride_offers.request_to_join()
        self.assertTrue(self.response['message']== "request accepted" or self.response['message']=="request decline")

        


    


