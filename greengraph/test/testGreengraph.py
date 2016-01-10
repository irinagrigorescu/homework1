import os
import yaml
import numpy as np
import unittest
from ..greengraph import Greengraph
from nose.tools import *
from mock import Mock, patch

'''
Class for testing Greengraph
'''
class TestGreengraph(unittest.TestCase):
    
    def setUp(self):
        '''
        Loading fixtures from samplesGreengraph.yaml file
        '''
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'samplesGreengraph.yaml')) as fixture_file:
            self.fixtures = yaml.load(fixture_file)

    def test_geolocate(self):
        '''
        Going through all the testcases for the geolocate method
        '''
        for testcase in self.fixtures['geolocate']:
            location = testcase.pop('location')
            answer = (testcase.pop('anslat'), testcase.pop('anslong'))
            
            geo_attr = {'geocoder.geocode.return_value' : answer}
            geo = Mock(**geo_attr)
            assert_equal(geo.geocoder.geocode(location), answer)

    def test_location_sequence(self):
        '''
        Going through all the testcases for the location_sequence method
        '''
        for testcase in self.fixtures['location_sequence']:
            start = tuple(testcase.pop('start'))
            end = tuple(testcase.pop('end'))
            steps = testcase.pop('steps')
            answer = np.vstack(testcase.pop('answer'))
            
            geo = Greengraph(0, 0)
            return_val = geo.location_sequence(start, end, steps)
            assert(np.array_equal(return_val, answer))

    def test_green_between(self):
        '''
        pass
        '''
        pass

if __name__ == "__main__":
    unittest.main()
