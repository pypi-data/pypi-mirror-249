from src.foxlator_lib.stt.whisper_stt import WhisperSTT
from unittest.mock import MagicMock, patch
from utils import base


class WhisperSTTTests(base.TestBase):

    @patch('whisper.load_model')
    def test_init_default(self, _mock: MagicMock):
        whisper_stt = WhisperSTT()
        self.assertIsNotNone(whisper_stt.model)
        self.assertIsNotNone(whisper_stt.language)

    def test_init_correct_params(self):
        whisper_stt = WhisperSTT(language='pl', model='tiny')
        self.assertIsNotNone(whisper_stt.model)
        self.assertIsNotNone(whisper_stt.language)

    def test_init_invalid_model(self):
        with self.assertRaises(Exception):
            WhisperSTT(model='invalid_model')

    @patch('whisper.load_model')
    def test_init_invalid_language(self, _mock: MagicMock):
        with self.assertRaises(Exception):
            WhisperSTT(language='invalid_language')

    def test_audio_to_text_smoke(self):
        try:
            whisper_stt = WhisperSTT(model='tiny')
            whisper_stt.audio_to_text(self.stereo_audio_path)
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
