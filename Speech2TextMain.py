from ServerInteract import speech2text_wav
from os import listdir
from os.path import isfile, join
import re
from bcolors import bcolors
import time

SoundWavDir = "./wav/"
TextDir = "./text/"
BeginCount = 1
soundfiles = [f for f in listdir(SoundWavDir) if isfile(join(SoundWavDir, f))]
textfiles = [f for f in listdir(TextDir) if isfile(join(TextDir, f))]

if __name__ == '__main__':
    while True:
        for soundfile in soundfiles:
            try:
                file_index = re.findall(r"\d+", soundfile)[0]
                if int(file_index) < BeginCount:
                    continue
                textfilename = "%d.txt" % int(file_index)
                if textfilename in textfiles:
                    print(bcolors.WARNING + "record%d.wav already processed, skip" % int(file_index) + bcolors.ENDC)
                    continue
                soundfile_path = SoundWavDir + "record%d.wav" % int(file_index)
                try:
                    text_result = speech2text_wav(soundfile_path)
                except Exception as e:
                    print(bcolors.WARNING + "Encouter error", e, bcolors.ENDC)
                    continue
                if len(text_result) < 1:
                    print(bcolors.WARNING + "Encouter error", e, bcolors.ENDC)
                    continue
                print(bcolors.HEADER + "Writing Text to %d.txt." % int(file_index))
                with open(TextDir + "%d.txt" % int(file_index), "w") as f:
                    f.write(text_result)
                    f.close()
            except IndexError:
                print("No Sound Files")

        print("Round finished. Sleep 30 seconds!")
        time.sleep(30)
        soundfiles = [f for f in listdir(SoundWavDir) if isfile(join(SoundWavDir, f))]
        textfiles = [f for f in listdir(TextDir) if isfile(join(TextDir, f))]

