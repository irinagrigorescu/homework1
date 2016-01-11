import os
import yaml
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

    '''
    Testing geolocate
    '''
    def test_geolocate(self):
        '''
        Mock function for geocode method in GoogleV3
        '''
        print "test_geolocate"
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
    
    '''
    Testing location_sequence
    '''
    def test_location_sequence(self):
        from numpy import array, array_equal
        gg = greengraph.Greengraph('Lima', 'Caracas')

        print "test_location_sequence"
        for test_case in self.fixtures['location_sequence']:
            print test_case
            start_coords = self.fixtures['geocode'][test_case['start']]
            end_coords = self.fixtures['geocode'][test_case['end']]
            print start_coords
            ans = gg.location_sequence(
                    (start_coords['lat'], start_coords['long']),
                    (end_coords['lat'], end_coords['long']),
                    test_case['steps'])
            '''
            Check result of location_sequence
            '''
            assert(array_equal(array(test_case['answer']), ans))

    '''
    Testing green_between
    '''
    def test_green_between(self):
        print "test_green_between"
        '''
        Create mock function for geocode
        '''
        with patch.object(greengraph.geopy.geocoders.GoogleV3, "geocode",
                side_effect = self.geocode_side_effect) as mock_geocode, \
             patch.object(greengraph, "Map") as mock_map:
            for test_case in self.fixtures["green_between"]:
                '''
                Create a new greengraph for each test_case
                '''
                gg = greengraph.Greengraph(test_case['start'], test_case['end'])
                for steps, correct_answer in test_case['steps'].iteritems():
                    '''
                    Create mock function with expected return results
                    for Map.count_green
                    '''
                    with patch.object(mock_map.return_value, "count_green",
                            side_effect=correct_answer) as mock_count_green:
                        answer = gg.green_between(steps)
                        assert(answer == correct_answer)
        

if __name__ == "__main__":
    unittest.main()
