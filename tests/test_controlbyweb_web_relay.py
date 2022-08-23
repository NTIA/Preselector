import unittest
from unittest.mock import MagicMock, PropertyMock

import defusedxml.ElementTree as ET
from requests import Response, codes

from its_preselector.controlbyweb_web_relay import ControlByWebWebRelay


class ControlByWebWebRelayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = (
            "<datavalues>"
            "<digitalInput1>0</digitalInput1>"
            "<digitalInput2>0</digitalInput2>"
            "<digitalInput3>0</digitalInput3>"
            "<digitalInput4>0</digitalInput4>"
            "<relay1>1</relay1>"
            "<relay2>1</relay2>"
            "<relay3>0</relay3>"
            "<relay4>0</relay4>"
            "<vin>27.6</vin>"
            "<register1>0</register1>"
            "<oneWireSensor1>102.3</oneWireSensor1>"
            "<utcTime>9160590</utcTime>"
            "<timezoneOffset>-25200</timezoneOffset>"
            "<serialNumber>00:0C:C8:05:AA:89</serialNumber>"
            "</datavalues>"
            ""
        )

    def test_is_enabled(self):
        web_relay = ControlByWebWebRelay(
            {"base_url": "127.0.0.1", "name": "test_switch"}
        )
        relay1_enabled = web_relay.is_enabled(self.state, "relay1")
        self.assertTrue(relay1_enabled)
        relay3_enabled = web_relay.is_enabled(self.state, "relay3")
        self.assertFalse(relay3_enabled)

    # def test_get_relay_summary(self):
    #   web_relay = ControlByWebWebRelay({"noise_diode_off" : "1State=1,2State=0,3State=0,4State=0"})
    #  summary = web_relay.get_state_summary(self.state)
    # self.assertEqual(summary, "1State=1,2State=0,3State=0,4State=0")

    def test_state_matches(self):
        root = ET.fromstring(self.state)
        web_relay = ControlByWebWebRelay(
            {
                "base_url": "127.0.0.1",
                "name": "test_switch",
                "control_states": {
                    "noise_diode_off": "1State=1,2State=0,3State=0,4State=0"
                },
            }
        )
        self.assertTrue(web_relay.state_matches("relay1=1", root))

    def test_get_state_from_config(self):
        root = ET.fromstring(self.state)
        web_relay = ControlByWebWebRelay(
            {
                "base_url": "127.0.0.1",
                "name": "test_preselector",
                "control_states": {
                    "noise_diode_off": "1State=1,2State=0,3State=0,4State=0"
                },
                "status_states": {
                    "noise diode powered": "relay2=1",
                    "antenna path enabled": "relay1=0",
                    "noise diode path enabled": "relay1=1",
                    "noise on": "relay2=1,relay1=1",
                    "measurements": "relay1=0,relay2=0,relay3=0,relay4=0",
                },
            }
        )
        response = Response()
        response.status_code = codes.ok
        type(response).text = PropertyMock(return_value=self.state)
        web_relay.get_state_xml = MagicMock(return_value=response)
        states = web_relay.get_status()
        self.assertEqual(len(states.keys()), 7)
        self.assertTrue(states["noise diode powered"])
        self.assertFalse(states["antenna path enabled"])
        self.assertFalse(states["measurements"])
        self.assertTrue(states["noise diode path enabled"])
        self.assertTrue(states["noise on"])

    def test_get_status(self):
        web_relay = ControlByWebWebRelay(
            {
                "base_url": "127.0.0.1",
                "name": "test preselector",
                "control_states": {
                    "noise_diode_off": "1State=1,2State=0,3State=0,4State=0"
                },
                "status_states": {
                    "noise diode powered": "relay2=1",
                    "antenna path enabled": "relay1=0",
                    "noise diode path enabled": "relay1=1",
                    "noise on": "relay2=1,relay1=1",
                    "measurements": "relay1=0,relay2=0,relay3=0,relay4=0",
                },
            }
        )
        response = Response()
        response.status_code = codes.ok
        type(response).text = PropertyMock(return_value=self.state)
        web_relay.get_state_xml = MagicMock(return_value=response)
        states = web_relay.get_status()
        self.assertEqual(len(states.keys()), 7)
        self.assertTrue(states["noise diode powered"])
        self.assertFalse(states["antenna path enabled"])
        self.assertFalse(states["measurements"])
        self.assertTrue(states["noise diode path enabled"])
        self.assertTrue(states["noise on"])


if __name__ == "__main__":
    unittest.main()
