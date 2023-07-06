import matplotlib
matplotlib.use('Agg')

import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


wavname = "grabacionALTA"
data, samplerate = sf.read(wavname + ".wav")
supposed = samplerate*5
slices = np.arange(np.size(data))

newData = np.multiply(data, 5)
newData /= np.max(np.abs(newData),axis=0)

print(samplerate)
print(np.size(data))
print(slices)
print(data)
print(newData)

""" plt.plot(slices, newData, slices, data)
plt.xlabel("Time")
plt.ylabel("Amplitude")

plt.savefig("figurejoin.pdf") """

fft_wave = np.fft.fft(data)
new_fft_wave = np.fft.fft(newData)

freqs = np.fft.fftfreq(len(data))

""" plt.plot(freqs, new_fft_wave, freqs, fft_wave)
plt.title("FFT of the signal")
plt.xlabel('Frequency')
plt.ylabel('Power of Frequency')
plt.xlim(-0.2, 0.2)
plt.savefig("figureFreq.pdf") """


sf.write('amplifiedGrabacion.wav', newData, samplerate)

plt.plot(np.abs(new_fft_wave)/np.size(newData))
plt.savefig("figureFrequencies.pdf")