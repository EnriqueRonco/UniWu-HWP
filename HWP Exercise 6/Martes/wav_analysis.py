import matplotlib
matplotlib.use('Agg')

import sys
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

def plotToPDF(x, y, xlabel, ylabel, title):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    pdfname = removeWhitespace(title)
    plt.savefig(pdfname + ".pdf")
    plt.close()

def removeWhitespace(string):
    return string.replace(" ", "")

wavname = sys.argv[1]
data, samplerate = sf.read(wavname + ".wav")

# Duration of the audio in seconds
length = data.shape[0] / samplerate

# Time array for representation
time = np.linspace(0., length, data.shape[0])

# Plot signal
plotToPDF(time, data, "Time (s)", "Amplitude", "Time domain signal")

# Multiply signal data by a scalar
amplifiedData = np.multiply(data, 5)

# Then normalize to [-1, +1]
amplifiedData /= np.max(np.abs(amplifiedData),axis=0)

# Write to WAV file the amplified signal
sf.write(wavname + 'Amplified.wav', amplifiedData, samplerate)

# Plot amplified signal
plotToPDF(time, amplifiedData, "Time (s)", "Amplitude", "Time domain amplified signal")

# Apply Fourier transform to both signals
transform = np.fft.fft(data)
amplifiedTransform = np.fft.fft(amplifiedData)

# Obtain frequencies
freqs = np.fft.fftfreq(transform.size, 1/float(samplerate))

# Plot transformed signals
plotToPDF(freqs, transform, "Frecuency (Hz)", "Amplitude", "Frequency domain signal")
plotToPDF(freqs, amplifiedTransform, "Frecuency (Hz)", "Amplitude", "Frequency domain amplified signal")

# Low-pass filter the amplified transformed signal (not working properly)
threshold = np.amax(amplifiedTransform)*0.05
filteredTransform = np.copy(amplifiedTransform)
filteredTransform[abs(amplifiedTransform) < threshold] = 0

# Plot filtered transformed signal
plotToPDF(freqs, filteredTransform, "Frecuency (Hz)", "Amplitude", "Frequency domain filtered signal")

# Transform filtered signal to time domain
filteredData = np.fft.ifft(filteredTransform)

# Write to WAV file the filtered signal
sf.write(wavname + 'Filtered.wav', filteredData.real, samplerate)

# Plot filtered signal
plotToPDF(time, filteredData, "Time (s)", "Amplitude", "Time domain filtered signal")