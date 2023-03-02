import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import IPython.display as ipd
from pydub import AudioSegment

def read_sound(f, frame_rate=44100, normalized=True): # Code from https://shonen-archive.tistory.com/5
    a = AudioSegment.from_file(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = np.sum(y.reshape((-1, 2)), axis=1)
    y = (np.float32(y) / 2**15)
    y = librosa.core.resample(y, a.frame_rate, frame_rate)
    return y, frame_rate


class SoundData:
    def __init__(self, path = None, n_fft = 1024, label="", frame_rate=44100, autoupdate = True):
        self.label = label
        self.n_fft = n_fft
        self.raw = np.array([])
        self.fourier = np.array([])
        self.amp = np.array([])
        self.db = np.array([])
        self.sr = 0
        if path:
            self.load(path, frame_rate)
            if autoupdate:
                self.update()
        
    def load(self, path, frame_rate=44100):
        self.raw, self.sr = read_sound(path, frame_rate)
        print(f"DataShape: {self.raw.shape}, frame rate={self.sr}")
        
    def update(self):
        self.fourier = librosa.core.stft(self.raw, n_fft=self.n_fft)
        self.amp = np.abs(self.fourier)
        self.db = librosa.amplitude_to_db(self.amp)
        
    def show(self, dur=800, off=0, title=None):
        plt.figure(figsize=(14, 3))
        librosa.display.specshow(self.db[:,off:off + dur], sr = self.sr)
        if title == None:
            title = "Spectogram" + ("" if self.label == "" else " of " + self.label)
        plt.title(title)
        plt.show()
    
    def copy(self):
        ret = SoundData(n_fft = self.n_fft, label = self.label)
        ret.raw = self.raw.copy()
        ret.update()
        ret.sr = self.sr
        return ret
    
    def play(self, ofs=0, dur=None):
        if dur == None : dur = self.raw.shape[0]
        ipd.display(ipd.Audio(self.raw[ofs:ofs+dur], rate=self.sr))
    
    def sync(A, B, search_length = 800, sample_length = 1500, sample_offset = 0, show_process=False):
        dotproductIndex = list(range(-(search_length//2), search_length//2))
        dotproduct = []
        average_A = np.average(np.sum(A.db, axis=0))
        average_B = np.average(np.sum(B.db, axis=0))
        for offset in range(-(search_length//2), (search_length//2)):
            offset_A = max(0, offset)
            offset_B = max(0, -offset)
            sample_A = A.db[:, sample_offset + offset_A:sample_offset + sample_length + offset_A]
            sample_B = B.db[:, sample_offset + offset_B:sample_offset + sample_length + offset_B]
            dotproduct.append(
                np.dot(
                    np.sum(sample_A, axis=0) - average_A,
                    np.sum(sample_B, axis=0) - average_B
                ) / (sample_length * A.n_fft)
            )
        if show_process:
            plt.plot(dotproductIndex, dotproduct)
            plt.title("Dot product")
            plt.xlabel("offset")
            plt.ylabel("dot product value")
            plt.show()
        
        offset = dotproduct.index(max(dotproduct)) - (search_length//2)
        print("offset: " + str(offset))
        offset_A = max(0, offset)
        offset_B = max(0, -offset)
        
        if show_process:
            plt.figure(figsize=(14, 3))
            plt.plot(np.average(A.db[:, sample_offset + offset_A:sample_offset + sample_length + offset_A],
                                axis=0), label=A.label)
            plt.plot(np.average(B.db[:, sample_offset + offset_B:sample_offset + sample_length + offset_B],
                                axis=0), label=B.label)
            plt.title("Amplitude")
            plt.legend()
            plt.show()
            
        newA = A.copy()
        newB = B.copy()
        newA.raw = librosa.core.istft(A.fourier[:, offset_A:])
        newB.raw = librosa.core.istft(B.fourier[:, offset_B:])
        minlength = min(newA.raw.shape[0], newB.raw.shape[0])
        newA.raw = newA.raw[:minlength]
        newB.raw = newB.raw[:minlength]
        newA.update()
        newB.update()
        return newA, newB
    
    
    