import json
import unittest
from pathlib import Path

from its_preselector.configuration_exception import ConfigurationException
from its_preselector.web_relay_preselector import WebRelayPreselector


class TestWebRelayPreselector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fpath = Path(__file__).parent.resolve()
        file = open(fpath / "test_metadata.sigmf-meta")
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(
            sensor_def, {"base_url": "127.0.0.1", "name": "test_switch"}
        )
        null_file = open(fpath / "null_preselector.sigmf-meta")
        null_def = json.load(null_file)
        null_file.close()
        cls.empty_preselector = WebRelayPreselector(
            null_def, {"base_url": "127.0.0.1", "name": "test_switch"}
        )
        with open(fpath / "sensor_definition.json") as f:
            sensor_def = json.load(f)
        cls.scos_preselector = WebRelayPreselector(
            sensor_def, {"name": "scos preselector", "base_url": "http://127.0.0.1"}
        )

    def test_requires_name(self):
        with self.assertRaises(ConfigurationException):
            exception_preselector = WebRelayPreselector({}, {"base_url": "127.0.0.1"})

    def test_requires_base_url(self):
        with self.assertRaises(ConfigurationException):
            exception_preselector = WebRelayPreselector({}, {"name": "test_name"})

    def test_valid_preselector(self):
        self.assertIsNotNone(self.preselector)

    def test_empty_preselector(self):
        self.assertIsNotNone(self.empty_preselector)

    def test_empty_valid_frequency_low_passband(self):
        self.assertEqual(
            3000000000.0, self.preselector.get_frequency_low_passband("noise_diode_on")
        )
        self.assertEqual(
            self.preselector.get_frequency_low_passband("noise_diode_on"),
            self.preselector.get_frequency_low_passband("antenna"),
        )

    def test_empty_get_frequency_low_passband(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_frequency_low_passband("noise_diode_on")

    def test_get_frequency_low_passband_bad_rf_path(self):
        with self.assertRaises(ConfigurationException):
            self.preselector.get_frequency_low_passband("BadRfPath")

    def test_valid_get_frequency_high_passband(self):
        self.assertEqual(
            3750000000.0, self.preselector.get_frequency_high_passband("noise_diode_on")
        )
        self.assertEqual(
            self.preselector.get_frequency_high_passband("noise_diode_on"),
            self.preselector.get_frequency_high_passband("antenna"),
        )

    def test_get_frequency_high_passband_bad_rf_path(self):
        with self.assertRaises(ConfigurationException):
            self.preselector.get_frequency_high_passband("BadRfPath")

    def test_empty_get_frequency_high_passband(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_frequency_high_passband("noise_diode_on")

    def test_valid_get_frequency_low_stopband(self):
        self.assertEqual(
            3550000000.0, self.preselector.get_frequency_low_stopband("noise_diode_on")
        )
        self.assertEqual(
            self.preselector.get_frequency_low_stopband("noise_diode_on"),
            self.preselector.get_frequency_low_stopband("antenna"),
        )

    def test_get_frequency_low_stopband_bad_rf_path(self):
        with self.assertRaises(ConfigurationException):
            self.preselector.get_frequency_low_stopband("BadRfPath")

    def test_empty_get_frequency_low_stopband(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_frequency_low_stopband("noise_diode_on")

    def test_valid_get_frequency_high_stopband(self):
        self.assertEqual(
            3700000000.0, self.preselector.get_frequency_high_stopband("noise_diode_on")
        )
        self.assertEqual(
            self.preselector.get_frequency_high_stopband("noise_diode_on"),
            self.preselector.get_frequency_high_stopband("antenna"),
        )

    def test_empty_get_frequency_high_stopband(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_frequency_high_stopband("noise_diode_on")

    def test_get_amplifier_gain(self):
        self.assertEqual(30, self.preselector.get_amplifier_gain("noise_diode_on"))

    def test_get_amplifier_gain_nonexistent_amp(self):
        with self.assertRaises(ConfigurationException):
            self.preselector.get_amplifier_gain("BadAmp")

    def test_empty_get_amplifier_gain(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_amplifier_gain(0)

    def test_get_amplifier_noise_figure(self):
        self.assertEqual(
            2.0, self.preselector.get_amplifier_noise_figure("noise_diode_on")
        )

    def test_empty_get_amplifier_noise_figure(self):
        with self.assertRaises(ConfigurationException):
            self.empty_preselector.get_amplifier_noise_figure("noise_diode_on")

    def test_scos_calibration_sources(self):
        self.assertEqual(1, len(self.scos_preselector.cal_sources))


if __name__ == "__main__":
    unittest.main()
