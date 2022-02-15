import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json


class TestCalSource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = open('metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {})
        null_file = open('null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        cls.empty_preselector = WebRelayPreselector(null_def, {})

    def test_valid_cal_source(self):
        cal_sources = self.preselector.cal_sources
        self.assertEqual(1, len(cal_sources))
        cal_source = cal_sources[0]
        self.assertEqual(14.6, cal_source.enr)
        self.assertEqual("Calibrated noise source", cal_source.type)

    def test_valid_cal_source_spec(self):
        spec = self.preselector.cal_sources[0].cal_source_spec
        self.assertEqual("SG53400067", spec.id)
        self.assertEqual("Keysight 346B", spec.model)
        self.assertEqual("https://www.keysight.com/en/pd-1000001299%3Aepsg%3Apro-pn-346B/noise-source-10-mhz-to-18-ghz-nominal-enr-15-db?cc=US&lc=eng",spec.supplemental_information)

if __name__ == '__main__':
    unittest.main()
