import unittest
import json
from pathlib import Path
from its_preselector.web_relay_preselector import WebRelayPreselector


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fpath = Path(__file__).parent.resolve()
        file = open(fpath / 'test_metadata.sigmf-meta')
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
        preselector =WebRelayPreselector(self.sensor_def, {
            'name': 'preselector',
            'base_url': 'http://bad_preselector.gov',
            'control_states': {"noise_diode_off": "1State=1,2State=0,3State=0,4State=0"},
            'status_states': {
                "noise diode powered": "relay2=1",
                "antenna path enabled": "relay1=0",
                "noise diode path enabled": "relay1=1",
                "noise on": 'relay2=1,relay1=1',
                "measurements": 'relay1=0,relay2=0,relay3=0,relay4=0'
            }})

        self.assertFalse(preselector.healthy())

    def test_get_status_bad_url(self):
        preselector = WebRelayPreselector(self.sensor_def, {
            'name': 'preselector',
            'base_url': 'http://bad_preselector.gov',
            'control_states': {"noise_diode_off": "1State=1,2State=0,3State=0,4State=0"},
            'status_states': {
                "noise diode powered": "relay2=1",
                "antenna path enabled": "relay1=0",
                "noise diode path enabled": "relay1=1",
                "noise on": 'relay2=1,relay1=1',
                "measurements": 'relay1=0,relay2=0,relay3=0,relay4=0'
            }})
        status = preselector.get_status()
        self.assertFalse(status['web_relay_healthy'])


if __name__ == '__main__':
    unittest.main()