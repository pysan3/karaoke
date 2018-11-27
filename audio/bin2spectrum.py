import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Spectrum:
    def __init__(self, bin_data, nframe):
        self.data = np.array(bin_data)
        self.nframe = nframe // 2
        self.fp = 1024
        self.window = np.hamming(self.fp)

    def normalization(self, small, large):
        # data numbers changed into floats within [0.00 - 0.99]
        self.data = (self.data - small) / (large - small + large * 0.01)

    def intoPixels(self):
        # returns a monotone spectrogram of audio_data (reversed)
        self.mono = np.empty([self.nframe // self.fp, self.fp//2+1])
        for i in range(0, self.nframe, self.fp):
            frame = self.data[i:i+self.fp]
            if len(frame) == self.fp:
                windowedData = self.window * frame
                fft_result = np.fft.rfft(windowedData)
                fft_data = np.log(np.abs(fft_result) ** 2)
                self.mono[i//self.fp] = fft_data[::-1]

    def len_mono(self):
        return self.mono.shape[0]

    def writeImage(self, dataname, width):
        mono_T = (self.mono.T) * 256
        diff = mono_T.shape[0] - int(mono_T.shape[0]/3)
        shape = (mono_T.shape[0] - diff, (192 if width != -1 else mono_T.shape[1]))
        mono_T = [[int(mono_T[i+diff][j+width]) for j in range(shape[1])] for i in range(shape[0])]
        color_shape = (shape[1]//3, shape[0])
        color_T = Image.new("RGB", color_shape)
        for i in range(shape[0]):
            for j in range(0, shape[1]//3):
                color_T.putpixel((j, i), tuple(mono_T[i][j*3:j*3+3]))
        file_number = "{:02d}".format((width//192)+1) if width != -1 else ".Spectrogram"
        color_T.save("./wav_split/" + dataname + "/" + file_number + ".png")
        if width == -1:
            color_T.show()
            print("done :", dataname)
            self.color = np.array(color_T).transpose(1,0,2)
            return self.color