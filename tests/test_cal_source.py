import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json
from pathlib import Path

class TestCalSource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fpath = Path(__file__).parent.resolve()
        file = open(fpath / 'test_metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {})
        null_file = open(fpath / 'null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        null_file.close()
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

    def test_empty_cal_source(self):
        self.assertIsNotNone(self.empty_preselector.cal_sources)
        self.assertEqual(0, len(self.empty_preselector.cal_sources))

if __name__ == '__main__':
    unittest.main()
