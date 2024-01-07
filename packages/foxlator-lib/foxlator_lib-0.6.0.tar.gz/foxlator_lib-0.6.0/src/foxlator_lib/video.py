import pathlib
import dataclasses
import typing
import os
import moviepy.editor as mp  # type: ignore
from moviepy.video.tools.subtitles import SubtitlesClip  # type: ignore

from .audio import AudioPath
from .error import BaseError


@dataclasses.dataclass
class SubtitleFrame:
    begin: int
    end: int
    text: str

    def serialize(self):
        return ((self.begin, self.end), self.text)


class VideoError(BaseError):
    pass


class Video(object):
    known_extensions = ['.mp4']

    def __init__(self, path: str):
        self.path = path
        self.extension = self._validate_extension(path)

        if (not os.path.isfile(path)):
            raise VideoError(f"Video file: '{path}' doesn't exist")
        self.clip: mp.VideoFileClip = mp.VideoFileClip(self.path)

    def apply_subtitles(self, subtitles: typing.List[SubtitleFrame], path: str):
        # TODO: make it all configurable (in next version?), research if there is any better way of
        # TODO: editing frames with timestamps (preferably compatible with opencv)
        def generator(text: str) -> mp.TextClip:
            return mp.TextClip(
                text, font='Arial', fontsize=24, color='white')
        subtitles_clip = SubtitlesClip(
            [subtitle.serialize() for subtitle in subtitles], generator)
        composed_clip = mp.CompositeVideoClip([
            self.clip, subtitles_clip.set_position(('center', 'bottom'))
        ])
        composed_clip.write_videofile(path + self.extension, logger=None)

    def get_audio_path(self) -> AudioPath:
        if self.clip.audio:
            return AudioPath(audio=self.clip.audio)
        raise VideoError(reason="Clip doesn't have audio path")

    def _validate_extension(self, path: str) -> str:
        extension: str = pathlib.Path(path).suffix
        if len(extension) == 0:
            raise VideoError(
                "Provided file path is invalid or doesn't contain extension")
        if extension not in self.known_extensions:
            raise VideoError(f"Unsupported file extension: {extension}")
        return extension
