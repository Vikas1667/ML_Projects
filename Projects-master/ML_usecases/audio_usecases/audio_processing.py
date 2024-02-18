from os import path
from pydub import AudioSegment

# files
# src = "./dataset/XC174949.ogg"
# dst = "./dataset/"

src = input("In: ")
dst = input("Out: ")

# convert mp3 to wav
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

