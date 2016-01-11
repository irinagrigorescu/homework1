import os
import yaml
import numpy as np
import unittest
from .. import greengraph
from nose.tools import *
from mock import Mock, patch

YAMLFILE = 'samplesGreengraph.yaml'

'''
Class for testing Greengraph
'''
class TestGreengraph(unittest.TestCase):
    
    def setUp(self):
        '''
        Setting up some attributes
        '''
        self.YAMLFILE = 'samplesGreengraph.yaml'
        self.ALLOWED_ERROR = 0.00001
        '''
        Loading fixtures from samplesGreengraph.yaml file
        '''
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', self.YAMLFILE)) as fixture_file:
            self.fixtures = yaml.load(fixture_file)

    '''
    Mock side effects for geocode based on values in self.fixtures
    '''
    def geocode_side_effect(self, place, exactly_one=False):
        from geopy.point import Point
        from geopy.location import Location

        if place in self.fixtures['geocode']:
            '''
            If it's not one of the locations defined in fixtures
            '''
            ans = self.fixtures['geocode'][place]
            return [Location(place, Point(ans['lat'], ans['long']))]
        else:
            '''
            Otherwise return some place in Antarctica
            '''
            return [Location((37.3890924, -5.9844589, 0.0))]

    def test_geolocate(self):
        '''
        Mock function for geocode method in GoogleV3
        '''
        with patch.object(greengraph.geopy.geocoders.GoogleV3, 'geocode',
                side_effect = self.geocode_side_effect) as mock_geocode:
            '''
            Context with mocked geocode
            '''
            gg = greengraph.Greengraph('Bogota', 'Montevideo')

            '''
            Test if geocode function is called with the expected arguments 
            and that geolocate returns the correct answer provided the
            assumed answer from geocode.
            '''
            for location, answer in self.fixtures['geocode'].iteritems():
                ans = gg.geolocate(location)
                mock_geocode.assert_called_with(location, exactly_one=False)
                assert(abs(ans[0] - answer["lat"]) < self.ALLOWED_ERROR)
                assert(abs(ans[1] - answer["long"]) < self.ALLOWED_ERROR)
       
    def test_location_sequence(self):
        pass
        '''
        Going through all the testcases for the location_sequence method
        '''
        '''
        for testcase in self.fixtures['location_sequence']:
            start = tuple(testcase.pop('start'))
            end = tuple(testcase.pop('end'))
            steps = testcase.pop('steps')
            answer = np.vstack(testcase.pop('answer'))
            
            geo = Greengraph(0, 0)
            return_val = geo.location_sequence(start, end, steps)
            assert(np.array_equal(return_val, answer))
        '''

    def test_green_between(self):
        '''
        pass
        '''
        pass

if __name__ == "__main__":
    unittest.main()
