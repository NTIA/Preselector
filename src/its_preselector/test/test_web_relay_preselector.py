import unittest
import json

from its_preselector.web_relay_preselector import WebRelayPreselector


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = open('test_metadata.sigmf-meta')
        cls.sensor_def = json.load(file)
        file.close()

    def test_blank_base_url(self):
        preselector = WebRelayPreselector(self.sensor_def,
                                          {'base_url': '', 'antenna': '1State=0,2State=0,3State=0,4State=0'})
        with self.assertRaises(Exception):
            preselector.set_state('antenna')

    def test_none_base_url(self):
        preselector = WebRelayPreselector(self.sensor_def,
                                          {'base_url': None, 'antenna': '1State=0,2State=0,3State=0,4State=0'})
        with self.assertRaises(Exception):
            preselector.set_state('antenna')

    def test_invalid_base_url(self):
        preselector = WebRelayPreselector(self.sensor_def, {'base_url': 'http://badpreselector.gov',
                                                            'antenna': '1State=0,2State=0,3State=0,4State=0'})
        with self.assertRaises(Exception):
            preselector.set_state('antenna')

    def test_healthy_false(self):
        preselector = WebRelayPreselector(self.sensor_def, {'base_url': 'http://bad_preselector.gov',
                                                            'antenna': '1State=0,2State=0,3State=0,4State=0'})
        self.assertFalse(preselector.healthy())


if __name__ == '__main__':
    unittest.main()
