from utils import base
import numpy as np
import tempfile
import os


class AudioPathTests(base.TestBase):

    def test_save_success(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.stereo_audio_path.save(tmp.name)
            self.assertTrue(os.path.exists(tmp.name + ".mp3"))

    def test_to_soundarray_stereo_audio(self):
        to_soundarray_value = self.stereo_audio_path.to_soundarray()
        self.assertEqual(to_soundarray_value.shape,
                         self.stereo_audio_array.shape)
        np.testing.assert_allclose(
            to_soundarray_value, self.stereo_audio_array, rtol=1e-3, atol=1e-3)

    def test_to_wave_soundarray_smoke(self):
        try:
            result = self.stereo_audio_path.to_wave_soundarray()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
        self.assertIsNotNone(result, "Result should not be None")
        self.assertTrue(result.ndim == 1)
