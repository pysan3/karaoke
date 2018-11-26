import numpy as np
import wave
from struct import unpack

import monauralize

class Audio:
    def __init__(self, filename):
        self.filename = filename
        self.audio_data = []

    #return audio file as array of integer
    def read(self):
        #read wav file
        wav = wave.open(self.filename, "r")

        #move to head of the audio file
        wav.rewind()

        self.nframe = wav.getnframes()
        self.rframe = wav.getframerate()
        self.channels = wav.getnchannels()
        self.sampwidth = wav.getsampwidth()
        print("nframe:{0}, rframe:{1}, channels:{2}, sampwidth:{3}".format(self.nframe, self.rframe, self.channels, self.sampwidth))

        # read to buffer as binary format
        buf = wav.readframes(self.nframe)
        wav.close()

        if self.sampwidth == 2:
            self.audio_data = np.frombuffer(buf, dtype="int16")
        elif self.sampwidth == 4:
            self.audio_data = np.frombuffer(buf, dtype="int32")
        elif self.sampwidth == 3:
            for i in range(len(buf)):
                try:
                    self.audio_data.append(unpack("<i", bytearray([0]) + buf[self.sampwidth * i:self.sampwidth * (i+1)])[0])
                except:
                    self.audio_data.append(0)
            self.audio_data = np.array(self.audio_data)

        # change to monaural data
        if self.channels != 1:
            self.audio_data = np.array(monauralize.monauralize(self.audio_data, self.nframe, self.channels))
            print("nframe changed :", len(self.audio_data))

    def length(self):
        return float(self.nframe/self.rframe)

    def length_short(self, N):
        return float(N / self.rframe)

    def split_write(self, count, N):
        w = wave.Wave_write("./wav_split/" + self.filename + "{:04d}.wav".format(count))
        w.setnchannels(self.channels)
        w.setsampwidth(self.sampwidth)
        w.setframerate(self.rframe)
        w.writeframes(self.audio_data[count*N:(count+1)*N])
        w.close()

    def split_data(self, count, N):
        return self.audio_data[count*N:(count+1)*N]

    def return_audio_data(self):
        return self.audio_data