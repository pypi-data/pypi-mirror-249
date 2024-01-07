
from typing import Any
from xmlrpc.client import Boolean
import moviepy.editor as mp  # type: ignore
import numpy as np
import io
from pydub import AudioSegment  # type: ignore
from scipy.io.wavfile import write  # type: ignore
from numpy.typing import NDArray
from .error import BaseError


class AudioError(BaseError):
    pass


class AudioPath(object):
    def __init__(self, audio: mp.AudioFileClip):
        self.audio_file_clip = audio

    def save(self, path: str):
        # TODO: consider taking codec/extensions as parameter instead of using .mp3
        self.audio_file_clip.write_audiofile(path + '.mp3', logger=None, )

    def to_soundarray(self,
                      tt: NDArray[np.floating[Any]] | None = None,
                      fps: int | None = None,
                      quantize: Boolean | None = False,
                      nbytes: int = 2,
                      buffersize: int = 50000,
                      ) -> NDArray[Any]:
        """These methods are an override of the to_soundarray method from moviepy.AudioClip due to the problems with numpy. 
        Transforms the sound into an stereo array.

        Args:
            tt (NDArray[np.floating[Any]] | None, optional): Time table. Defaults to None.
            fps (int | None, optional): Frame rate of the sound for the conversion (44100 for top quality). Defaults to None.
            quantize (Boolean | None, optional): Defaults to False.
            nbytes (int, optional): number of bytes to encode the sound: 1 for 8bit sound, 2 for 16bit, 4 for 32bit sound. Defaults to 2.
            buffersize (int, optional): buffersize. Defaults to 50000.
        """
        if fps is None:
            fps = self.audio_file_clip.fps
        duration = float(self.audio_file_clip.duration)  # type: ignore
        stacker = np.vstack if self.audio_file_clip.nchannels == 2 else np.hstack
        max_duration = 1.0 * buffersize / fps
        if tt is None:
            if duration > max_duration:
                return stacker(list(self.audio_file_clip.iter_chunks(fps=fps, quantize=quantize,
                                                                     nbytes=2, chunksize=buffersize)))
            else:
                tt = np.arange(0, duration, 1.0/fps)
        snd_array = self.audio_file_clip.get_frame(tt)
        if quantize:
            snd_array = np.maximum(-0.99, np.minimum(0.99, snd_array))
            inttype = {1: 'int8', 2: 'int16', 4: 'int32'}[nbytes]
            snd_array: NDArray[Any] = (
                2**(8*nbytes-1)*snd_array).astype(inttype)
        return snd_array

    def to_wave_soundarray(self, frame_rate: int = 16000, sample_width: int = 2, channels: int = 1, normalize: bool = False):
        audio_array = self.to_soundarray()
        audio_bytesio = io.BytesIO()
        # convert array to wave bytesio
        write(audio_bytesio, self.audio_file_clip.fps, audio_array)
        segment = AudioSegment.from_file_using_temporary_files(  # type: ignore
            io.BytesIO(audio_bytesio.getvalue()))
        if segment.frame_rate != frame_rate:  # type: ignore
            segment = segment.set_frame_rate(frame_rate)  # type: ignore
        if segment.sample_width != sample_width:  # type: ignore
            segment = segment.set_sample_width(sample_width)  # type: ignore
        if segment.channels != channels:  # type: ignore
            segment = segment.set_channels(channels)  # type: ignore
        arr = np.array(segment.get_array_of_samples())  # type: ignore
        if normalize:
            return arr.astype(np.float32)/32768.0
        return arr.astype(np.float32)
