import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json
from pathlib import Path


class TestWebRelayPreselector(unittest.TestCase):

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
        with open(fpath / 'sensor_definition.json', 'r') as f:
            sensor_def = json.load(f)
        cls.scos_preselector = WebRelayPreselector(sensor_def, {})

    def test_valid_preselector(self):
        self.assertIsNotNone(self.preselector)

    def test_empty_preselector(self):
        self.assertIsNotNone(self.empty_preselector)

    def test_empty_valid_frequency_low_passband(self):
        self.assertEqual(3000000000.0, self.preselector.get_frequency_low_passband(0))
        self.assertEqual(self.preselector.get_frequency_low_passband(0), self.preselector.get_frequency_low_passband(1))

    def test_empty_get_frequency_low_passband(self):
        self.assertIsNone(self.empty_preselector.get_frequency_low_passband(0))

    def test_valid_get_frequency_high_passband(self):
        self.assertEqual(3750000000.0, self.preselector.get_frequency_high_passband(0))
        self.assertEqual(self.preselector.get_frequency_high_passband(0),
                         self.preselector.get_frequency_high_passband(1))

    def test_empty_get_frequency_high_passband(self):
        self.assertIsNone(self.empty_preselector.get_frequency_high_passband(0))

    def test_valid_get_frequency_low_stopband(self):
        self.assertEqual(3550000000.0, self.preselector.get_frequency_low_stopband(0))
        self.assertEqual(self.preselector.get_frequency_low_stopband(0), self.preselector.get_frequency_low_stopband(1))

    def test_empty_get_frequency_low_stopband(self):
        self.assertIsNone(self.empty_preselector.get_frequency_low_stopband(0))

    def test_valid_get_frequency_high_stopband(self):
        self.assertEqual(3700000000.0, self.preselector.get_frequency_high_stopband(0))
        self.assertEqual(self.preselector.get_frequency_high_stopband(0),
                         self.preselector.get_frequency_high_stopband(1))

    def test_empty_get_frequency_high_stopband(self):
        self.assertIsNone(self.empty_preselector.get_frequency_high_stopband(0))

    def test_get_amplifier_gain(self):
        self.assertEqual(30, self.preselector.get_amplifier_gain(0))

    def test_empty_get_amplifier_gain(self):
        self.assertIsNone(self.empty_preselector.get_amplifier_gain(0))

    def test_get_amplifier_noise_figure(self):
        self.assertEqual(2.0, self.preselector.get_amplifier_noise_figure(0))

    def test_empty_get_amplifier_noise_figure(self):
        self.assertIsNone(self.empty_preselector.get_amplifier_noise_figure(0))

    def test_scos_calibration_sources(self):
        self.assertEqual(1, len(self.scos_preselector.cal_sources))


if __name__ == '__main__':
    unittest.main()
