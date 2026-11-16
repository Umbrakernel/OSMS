import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

sr = 1000
duration = 0.5

melody = """
la DO SOL FA MI RE DO MI
si DO SOL MI RE DO la sol LA SI RE si DO RE DO si la
la DO SOL FA MI RE DO MI si DO SOL MI RE DO LA
sol LA do
MI MI SOL FA MI RE DO RE RE DO MI
RE DO
MI MI SOL FA MI RE DO SOL SOL LA MI RE DO
la la si DO la la DO RE RE DO MI
MI MI RE DO RE DO RE DO LA
MI MI RE DO RE DO la1 DO RE MI FA MI RE
RE MI RE DO RE DO la1 DO RE MI FA MI RE
DO RE SOL SOL LA SOL RE
RE DO DO FA MI
MI MI RE DO RE DO
la sol la si DO RE DO si la
la DO SOL FA MI RE DO MI
si DO SOL MI RE DO la sol LA SI RE si DO RE DO si la
la DO SOL FA MI RE DO MI si DO SOL MI RE DO LA
sol LA do
"""

freq = {
    "do": 130.81, "re": 146.83, "mi": 164.81,
    "fa": 174.61, "sol": 196.00, "la": 220.00,
    "si": 246.94, "DO": 261.63, "RE": 293.66,
    "MI": 329.63, "FA": 349.23, "SOL": 392.00,
    "LA": 440.00, "SI": 493.88, "la1": 220.00
}

song = []

for note in melody.split():
    t = np.arange(int(sr * duration)) / sr
    sound = np.sin(2 * np.pi * freq[note] * t)
    song.extend(sound)

song = np.array(song)
song = (song * 32767).astype(np.int16)

write("listen_to_your_heart.wav", sr, song)

plt.plot(song[:2000])
plt.show()
