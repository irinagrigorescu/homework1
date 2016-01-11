import yaml
import unittest
from .. import map as app_map
from mock import patch
import requests

'''
Class for testing Map
'''
class TestMap(unittest.TestCase):

    '''
    Setup method
    '''
    def setUp(self):
        from os.path import join, dirname
        '''
        Setting up some attributes
        '''
        self.yamlfile = 'samplesMap.yaml'
        self.eps = 0.00001
        '''
        Loading fixtures from samplesMap.yaml file
        '''
        with open(join(dirname(__file__), 'fixtures', self.yamlfile)) as fixture_file:
            self.fixtures = yaml.load(fixture_file)

    '''
    Mock function from requests.get from google satellite
    '''
    def mock_requests_get(self, base, params={}):
        import numpy as np
        from StringIO import StringIO
        from matplotlib import image as img

        '''
        Dummy class where we can add the attribute "content"
        '''
        class Object(object):
            pass
        mock_result = Object()

        '''
        Get the target image size
        '''
        (w, h) = map(int, params.get("size", "400x400").split("x"))

        '''
        Creating a dummy array of the appropriate size.
        The array contains only zeros except in its 10x10 upper left corner.
        '''
        arr = np.zeros((h, w, 3), dtype = np.float32)
        for i,j in [(i,j) for i in range(10) for j in range(10)]:
            arr[i, j, 0] = i / 255.0;      # Red   ~ i
            arr[i, j, 1] = (i + j)/ 255.0; # Green ~ i+j
            arr[i, j, 2] = j / 255.0;      # Blue  ~ j

        '''
        Save the array as an image to a string
        in the field "content" of an object
        '''
        string_buffer = StringIO()
        img.imsave(string_buffer, arr, format="png")
        setattr(mock_result, "content", string_buffer.getvalue())
        string_buffer.close()

        return mock_result

    '''
    Testing test_green
    '''
    def test_green(self):
        with patch.object(requests, "get", 
                          side_effect=self.mock_requests_get) as mf:
            '''
            Mock function here
            '''
            my_map = app_map.Map(self.fixtures['long'], self.fixtures['lat'])

            for threshold in self.fixtures['thresholds']:
                bool_map = my_map.green(threshold)
                ''' 
                Check that the green pixels were correctly identified
                '''
                for i,j in [(i,j) for i in range(10) for j in range(10)]:
                    assert(bool_map[i, j] == 
                            (((i+j) > threshold*i) and (((i+j) > threshold*j))))

    '''
    Testing count_green
    '''
    def test_count_green(self):
        with patch.object(requests, "get",
                side_effect=self.mock_requests_get) as mf:
            my_map = app_map.Map(self.fixtures['long'], self.fixtures['lat'])
            
            '''
            Counting the number of green pixels for different thresholds
            '''
            r = map(my_map.count_green, self.fixtures['thresholds'])
            '''
            Checking the values
            '''
            assert(r == self.fixtures['green_no'])

    '''
    Testing show_green
    '''
    def test_show_green(self):
        import numpy as np
        from StringIO import StringIO
        from matplotlib import image as img

        with patch.object(requests, "get", 
                side_effect=self.mock_requests_get) as mf:
            my_map = app_map.Map(self.fixtures['long'], self.fixtures['lat'])
            thresholds = self.fixtures['thresholds']
            green_nos = self.fixtures['green_no']
            for threshold, green_no in zip(thresholds, green_nos):
                '''
                Get the green map
                '''
                green_array = img.imread(StringIO(my_map.show_green(threshold)))
                '''
                Check that the red and blue channels are black
                '''
                assert(np.all(green_array[:,:,0] == 0))
                assert(np.all(green_array[:,:,2] == 0))
                '''
                Check that the number of green pixels is correct
                '''
                assert(abs(np.sum(green_array[:,:,1]) - green_no) < self.eps)
                '''
                Check that the green pixels were correctly identified
                '''
                for i,j in [(i,j) for i in range(10) for j in range(10)]:
                    assert((green_array[i,j,1] == 1) == (((i+j) > threshold*i)
                        and ((i+j) > threshold*j)))

if __name__ == "__main__":
    unittest.main()
