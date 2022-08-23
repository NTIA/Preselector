import unittest
from its_preselector.web_relay_preselector import WebRelayPreselector
import json
from pathlib import Path


class TestAmplifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fpath = Path(__file__).parent.resolve()
        file = open(fpath / 'test_metadata.sigmf-meta')
        sensor_def = json.load(file)
        file.close()
        cls.preselector = WebRelayPreselector(sensor_def, {'base_url': 'http://127.0.0.1', 'name': 'test_preselector'})
        null_file = open(fpath / 'null_preselector.sigmf-meta')
        null_def = json.load(null_file)
        null_file.close()
        cls.empty_preselector = WebRelayPreselector(null_def, {'base_url': 'http://127.0.0.1', 'name': 'test_preselector'})

    def test_valid_amplifier(self):
        amplifiers = self.preselector.amplifiers
        self.assertEqual(1, len(amplifiers))
        amplifier = amplifiers[0]
        self.assertEqual(30, amplifier.gain)
        self.assertEqual(2.0, amplifier.noise_figure)
        self.assertEqual(10, amplifier.max_power)

    def test_valid_amplifier_spec(self):
        spec = self.preselector.amplifiers[0].amplifier_spec
        self.assertEqual("1502150", spec.id)
        self.assertEqual("MITEQ AFS44-00101800-25-10P-44", spec.model)
        self.assertEqual("https://nardamiteq.com/docs/MITEQ_Amplifier-AFS.JS_c41.pdf", spec.supplemental_information)

    def test_empty_amplifiers(self):
        self.assertIsNotNone(self.empty_preselector.amplifiers)
        self.assertEqual(0, len(self.empty_preselector.amplifiers))


if __name__ == '__main__':
    unittest.main()
