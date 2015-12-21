import yaml
import os
import numpy as np
from ..map import Map
from ..greengraph import Greengraph
from nose.tools import assert_equal

def test_geolocate():
	with open(os.path.join(os.path.dirname(__file__),'fixtures','samples.yaml')) as fixture_file:
		fixtures = yaml.load(fixture_file)['geolocate']
	for fix in fixtures:
		location = fix.pop('location')
		anslat = fix.pop('anslat')
		anslong = fix.pop('anslong')
		answer = (anslat, anslong)
		geo = Greengraph(0.0, 0.0)
		assert_equal(geo.geolocate(location), answer)
	
def test_location_sequence():
	with open(os.path.join(os.path.dirname(__file__),'fixtures','samples.yaml')) as fixture_file:
		fixtures = yaml.load(fixture_file)['location_sequence']
	for fix in fixtures:
		start = fix.pop('start')
		end = fix.pop('end')
		steps = fix.pop('steps')
		answer = fix.pop('answer')
		geo = Greengraph(0.0, 0.0)
		return_val = geo.location_sequence(geo.geolocate(start), geo.geolocate(end), steps)
		answer = np.vstack(answer)
		assert(np.array_equal(return_val, answer))

def test_green_between():
	with open(os.path.join(os.path.dirname(__file__),'fixtures','samples.yaml')) as fixture_file:
                fixtures = yaml.load(fixture_file)['green_between']
	for fix in fixtures:
		start = fix.pop('start')
		end = fix.pop('end')
		steps = fix.pop('steps')
		answer = fix.pop('answer')
		geo = Greengraph(start, end)
		assert_equal(geo.green_between(steps), answer)

def test_green():
	with open(os.path.join(os.path.dirname(__file__),'fixtures','samples.yaml')) as fixture_file:
		fixtures = yaml.load(fixture_file)['green']
	for fix in fixtures:
		lat = fix.pop('lat')
		lon = fix.pop('long')
		satellite = fix.pop('satellite')
		zoom = fix.pop('zoom')
		size = tuple(fix.pop('size'))
		matrixSize = size[0]*size[1]
		threshold = fix.pop('threshold')
		myths = fix.pop('myths')
		answer = fix.pop('answer')
		mapy = Map(lat, lon, satellite, zoom, size)
		greenMap = mapy.green(threshold)
		greenPixels = sum(sum(greenMap)) 
		assert((greenPixels >= myths*matrixSize) == answer)	

		

#test_geolocate()
#test_location_sequence()
#test_green_between()
#test_green()

#geo = Greengraph(2,4)
#print geo.location_sequence(geo.geolocate("London"), geo.geolocate("Bucharest"), 1)
#print geo.geolocate("Geneva")
#print geo.green_between(2)

mapy = Map(42, -38, satellite=True, zoom=10, size=(4,4))
a = mapy.count_green()
print a
#print sum(sum(a==True))

