import unittest
from typing import Any
from numpy.typing import NDArray
import tempfile
from moviepy.editor import AudioFileClip  # type: ignore
from scipy.io.wavfile import write  # type: ignore
import numpy as np
from src.foxlator_lib.audio import AudioPath

# any utility functions go here


class TestBase(unittest.TestCase):

    def setUp(self):
        self.audio_rate = 44100
        self.stereo_audio_array = np.random.uniform(
            -1, 1, (self.audio_rate*2, 2))
        self.stereo_audio_path = AudioPath(
            self.create_test_audio(self.stereo_audio_array))

    def create_test_audio(self, audio_array: NDArray[Any]):
        audio_rate = 44100
        with tempfile.NamedTemporaryFile() as tmp:
            write(tmp.name, audio_rate, audio_array)
            return AudioFileClip(tmp.name)
