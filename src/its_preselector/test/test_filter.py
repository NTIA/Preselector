import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json


class TestFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = open('test_metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {'base_url':'127.0.0.1', 'name': 'test_switch'})
        null_file = open('null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        null_file.close()
        cls.empty_preselector = WebRelayPreselector(null_def, {'base_url':'127.0.0.1', 'name': 'test_switch'})

    def test_valid_filter_spec(self):
        spec = self.preselector.filters[0].filter_spec
        self.assertEqual("13FV40, SN 9", spec.id)
        self.assertEqual("K&L 13FV40-3625/U150-o/o", spec.model)
        self.assertEqual("http://www.klfilterwizard.com/klfwpart.aspx?FWS=1112001&PN=13FV40-3625%2fU150-O%2fO",spec.supplemental_information)

    def test_valid_filter(self):
        self.assertEqual(1, len(self.preselector.amplifiers))
        amplifier = self.preselector.filters[0]
        self.assertEqual(3550000000.0,amplifier.frequency_low_stopband)
        self.assertEqual(3700000000.0, amplifier.frequency_high_stopband)
        self.assertEqual(3000000000.0, amplifier.frequency_low_passband)
        self.assertEqual(3750000000.0, amplifier.frequency_high_passband)

    def test_empty_filter(self):
        self.assertIsNotNone(self.empty_preselector.filters)
        self.assertEqual(0, len(self.empty_preselector.filters))


if __name__ == '__main__':
    unittest.main()
