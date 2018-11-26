import numpy as np
import glob
import os
import sys

import audio2bin
import bin2spectrum

def makeDirectory(filename):
    if os.path.isdir("./wav_split/{}".format(filename)):
        [os.remove(path) for path in glob.glob("./wav_split/{}/*".format(filename))]
    else:
        os.mkdir("./wav_split/{}".format(filename))

def writeText(spec_data, dataname):
    with open("./wav_text/{}.txt".format(dataname), "w") as f:
        for i in range(len(spec_data)):
            for k in range(3):
                for j in range(len(spec_data[i])-1, -1, -1):
                    f.write("{}, ".format(spec_data[i][j][k]))
                f.write("\n")

def makeSpectrogram(dataname):
    filename = "./wav/" + dataname + ".wav" # filename
    print("fetched \"{}\"".format(filename))
    au = audio2bin.Audio(filename)
    au.read()
    audio_wave = au.return_audio_data()
    print("audio2bin : done")
    makeDirectory(dataname)
    sp = bin2spectrum.Spectrum(audio_wave, au.nframe)
    sp.normalization(min(audio_wave), max(audio_wave))
    sp.intoPixels()
    print("outputting {} images".format(sp.len_mono()//192))
    for i in range(sp.len_mono()//192):
        sp.writeImage(dataname, i*192)
    return sp.writeImage(dataname, -1)

def main():
    filenames = glob.glob("./wav/*.wav")
    for filename in filenames:
        dataname = filename[6:-4]
        print("")
        print(dataname)
        spec_data = makeSpectrogram(dataname)
        writeText(spec_data, dataname)

if __name__ == "__main__":
    main()