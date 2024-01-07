
from ddt import ddt, data  # type: ignore
from unittest.mock import MagicMock, patch
from utils import base
from src import foxlator_lib as fll


@ddt
class VideoTests(base.TestBase):
    invalid_paths = ['path-without-extension',
                     'path.mp3', 'path.jpg', 'relative/path/file.obj']

    @patch('os.path.isfile')
    def test_when_creating_video_from_not_existing_path_should_throw_error(self, mock_isfile: MagicMock):
        path = 'some-path.mp4'
        mock_isfile.return_value = False
        self.assertRaises(fll.video.VideoError, lambda: fll.video.Video(path))
        mock_isfile.assert_called_once_with(path)

    @data(*invalid_paths)
    @patch('os.path.isfile')
    def test_when_creating_video_from_path_with_not_supported_extensions_should_throw_error(self, path: str, mock_isfile: MagicMock):
        mock_isfile.return_value = None
        self.assertRaises(fll.video.VideoError, lambda: fll.video.Video(path))
        mock_isfile.assert_not_called()
