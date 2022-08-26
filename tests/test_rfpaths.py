import json
import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
from pathlib import Path


class TestRFPaths(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fpath = Path(__file__).parent.resolve()
        file = open(fpath / 'test_metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {'base_url':'127.0.0.1', 'name': 'test_switch'})
        null_file = open(fpath / 'null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        null_file.close()
        cls.empty_preselector = WebRelayPreselector(null_def, {'base_url':'127.0.0.1', 'name': 'test_switch'})

    def test_number_valid_paths(self):
        self.assertEqual(2, len(self.preselector.rf_paths))

    def test_empty_paths(self):
        self.assertIsNotNone(self.empty_preselector.rf_paths)
        self.assertEqual(0, len(self.empty_preselector.rf_paths))

    def test_name(self):
        self.assertEqual('noise_diode_on', self.preselector.rf_paths["noise_diode_on"].name)

    def test_cal_source_id(self):
        self.assertEqual('SG53400067', self.preselector.rf_paths["noise_diode_on"].cal_source_id)

    def test_filter_id(self):
        self.assertEqual('13FV40, SN 9', self.preselector.rf_paths["noise_diode_on"].filter_id)

    def test_amplifier_id(self):
        self.assertEqual('1502150', self.preselector.rf_paths["noise_diode_on"].amplifier_id)


if __name__ == '__main__':
    unittest.main()

