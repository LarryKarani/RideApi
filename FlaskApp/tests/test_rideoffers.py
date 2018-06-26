import unittest
from FlaskApp.api.rideoffers import RideOffer

class RideOfferTestCase(unittest.TestCase):
    def setUp(self):
        self.rideoffer = RideOffer()
    def tearDown(self):
        RideOffer.ride_offers.clear()

    

    def test_create_ride_offer(self):
        self.response = self.rideoffer.create_ride(
            'larry', 'mombasa', 'kirinyaga', '10:30', 
            '29/10/2018', '$80/km', 'Thika road', 
            
        )
        self.assertIn(self.response, self.rideoffer.ride_offers)

    def test_get_a_ride_offer(self):
        self.response_in = self.rideoffer.create_ride(
            'larry', 'Tanzania', 'wakanda', '10:30', 
            '29/10/2018', '$80/km', 'Thika road', 
            
        )
        self.response_out = self.rideoffer.get_specific_offer(self.response_in['id'])
        self.assertIn(self.response_out, self.rideoffer.ride_offers)
    
    def test_get_all_ride_offers(self):
        self.response = self.rideoffer.get_all_rides()
        self.assertTrue(len(self.response)==len(self.rideoffer.ride_offers))

        


    


