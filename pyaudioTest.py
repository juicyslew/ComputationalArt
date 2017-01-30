from scipy.io.wavfile import read

musfile = "music/song.wav"
wavData = scipy.io.wavfile.read(musfile)

print(wavData)
