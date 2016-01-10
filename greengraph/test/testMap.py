import os
import yaml
import numpy as np
import unittest
from ..map import Map
from nose.tools import *
from mock import Mock, patch

class TestMap(unittest.TestCase):
    
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'samplesMap.yaml')) as fixture_file:
            self.fixtures = yaml.load(fixture_file)

    def test_green(self):
        pass

    def test_count_green(self):
        pass

    def test_show_green(self):
        pass

if __name__ == "__main__":
    unittest.main()
