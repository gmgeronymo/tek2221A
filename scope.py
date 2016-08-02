# Comunicar com osciloscopio Tek 2221A

# O programa utiliza a biblioteca pyVISA
import visa
import datetime
import numpy
import matplotlib.pyplot as plt

tdiv = 2e-6; # base de tempo

rm = visa.ResourceManager()

scope = rm.open_resource("GPIB0::4::INSTR")

inst = rm.open_resource('GPIB0::4::INSTR')
inst.write('INI')
inst.write('OPC ON;DAT CHA:CH1;ACQ CURR:AVE;ACQ NUM:4;ACQ TRIGC:512')
inst.timeout = 50000
inst.write('DAT ENC:ASC')
data = inst.query('WAV?')
data = data.split(',') # transforma em array

data[21] = data[21].replace('CRVCHK:CHKSM0;CURVE ','') # trata o primeiro elemento
data[len(data)-1] = data[len(data)-1].replace(';','') # trata o último elemento

ymult = float(data[14].replace('YMULT:',''))

waveform = []
for a in range(21,len(data)):
    waveform.append(float(data[a]))

waveform = numpy.array(waveform)


waveform = (waveform * ymult)
offset = ((waveform.max() - waveform.min()) / 2) + waveform.min()
waveform = waveform - offset

t = numpy.arange(0,tdiv*10,(tdiv*10)/1024)
t = t*1e6; # micro segundos

plt.plot(t,waveform)
plt.xlabel('time [$\mu$s]')
plt.ylabel('voltage [V]')
plt.grid(True)
plt.savefig("scope.png")
plt.show()

