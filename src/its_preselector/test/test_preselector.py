import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json


class TestWebRelayPreselector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = open('metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {})
        null_file = open('null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        null_file.close()
        cls.empty_preselector = WebRelayPreselector(null_def, {})

    def test_valid_preselector(self):
        self.assertIsNotNone(self.preselector)

    def test_empty_preselector(self):
        self.assertIsNotNone(self.empty_preselector)

if __name__ == '__main__':
    unittest.main()
