import yaml
import unittest
from ..greengraph import Greengraph
from nose.tools import *
from mock import Mock, patch

class TestGreengraph(unittest.Testcase):
    
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'samplesGreengraph.yaml')) as fixture_file:
            self.fixtures = yaml.load(fixture_file)

    def test_geolocate(self):
        pass

    def test_location_sequence(self):
        pass

    def test_green_between(self):
        pass

in __name__ == "__main__":
    unittest.main()
