from tkinter import *
from tkinter import Button
from tkinter import Entry,StringVar
from tkinter import filedialog
from tkinter import Label
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from scipy import signal
from scipy.fftpack import fft
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pylab as plt
import pyaudio
import scipy.io.wavfile as wavfile
import sys
import wave


sf = 0; 
###############################################################################
def IMPORTAR():
    #inicializacion de variables
    global a
    a = 0
    #abrimos carpeta
    file_path = filedialog.askopenfilename()
    print(file_path)
    Fs, dato = wavfile.read(file_path)
    scaled = np.int16(dato)
    #abrir en archivo
    write(("primer.wav"), Fs, scaled)

    Bajo1.set(1)
    Bajo2.set(1)
    Medio1.set(1)
    Medio2.set(1)
    Alto1.set(1)
    Alto2.set(1)
    Volumen.set(1)

###############################################################################
def GUARDAR():
    #inicializacion de variables
    global Fs, sf
    
    
    #guardar enarchivo
    filename = asksaveasfilename(initialdir = "/", title = "Save as",
                                 filetypes = (("audio file", ".wav"), ("all files", ".*")),
                                 defaultextension = ".wav")
    print(filename)
    scaled = np.int16(sf)
    write(filename, Fs, scaled)
    
###############################################################################
def GRABAR():
    #inicializacion de variables
    global a, entradaU, txtusuario, rec
    #iniciar ventana emergente 
    rec=Tk()
    #tamaño
    rec.geometry("260x100+500+200")
    #titulo
    rec.title("Grabar")
    #variable que se escribe
    entradaU = StringVar(rec)
    entradaU.set(" ")
    #ubicacion de ventana de texto
    txtusuario = Entry(rec, textvariable = entradaU).place(x = 50,y = 13)
    #ubicacion, nombre y color del boton
    btnGrabar = Button(rec, text = "Grabar", command = REC, font = ("Arial", 12)).place(x = 85,y = 50)
    #cierre de programa
    rec.mainloop() 
    
###############################################################################     
def REC():
    
    #cierre de ventana emergente
    
    #inicializacion de variables
    global entradaU, txtusuario, a, rec
    rec.destroy()
    a = 0
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = int(entradaU.get()) + 1
    samples = (44100 / 1024) * RECORD_SECONDS
    #grabar audio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate =RATE,input=True,frames_per_buffer=chunk)   
    print ("Grabando...")
    x = []
    for i in range(0, int(samples)):
            data = stream.read(chunk)
            x.append(data)
    print ("Fin de grabacion")
    #fin de grabacion      
    stream.stop_stream()
    stream.close()
    #guardar archivo
    wf = wave.open('primer.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(x))
    wf.close()
     
    Bajo1.set(1)
    Bajo2.set(1)
    Medio1.set(1)
    Medio2.set(1)
    Alto1.set(1)
    Alto2.set(1)
    Volumen.set(1)
    
###############################################################################
def FILTRO():
    #inicializacion de variables
    global b1, b2, m1, m2, a1, a2, sf, Fs, vol
    #filtros
    bajo1 = float(Bajo1.get())
    bajo2 = float(Bajo2.get())
    medio1 = float(Medio1.get())
    medio2 = float(Medio2.get())
    alto1 = float(Alto1.get())
    alto2 = float(Alto2.get())
    vol = float(Volumen.get())
    #abrir archivo
    Fs, y = wavfile.read("primer.wav")
    N = len(y)
    #inicio de filtro
    T = 1.0 / Fs
    x = np.linspace(0.0, N * T, N)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
    #Filtro
    nyq = Fs * 0.5
    
    #primer filtro bajo1
    cutoff = 125
    print('Frecuencia de corte', cutoff)
    
    stopfreq = float(cutoff)
    cornerfreq = 0.4 * stopfreq
    
    ws = cornerfreq / nyq
    wp = stopfreq / nyq
    N1, wn = signal.buttord(wp, ws, 3, 40)
    b, a = signal.butter(N1, wn, btype='low')
    
    b1 = signal.lfilter(b, a, y) * bajo1
    
    #filtro 2 bajo 2
    lowcut = 175
    highcut = 325
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    b2 = signal.lfilter(b, a, y) * bajo2   
    
    #filtro 3 medio 1
    lowcut = 350
    highcut = 650
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    m1 = signal.lfilter(b, a, y) * medio1
    
    #filtro 4 medio 2
    lowcut = 700
    highcut = 1300
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    m2 = signal.lfilter(b, a, y) * medio2
    
    #filtro 5 altos 1
    lowcut = 700
    highcut = 1300
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order,[ low,high ], btype = 'bandpass')
    
    a1 = signal.lfilter(b, a, y) * alto1
    
    #filtro 6 altos 2
    cutoff= 4000
    stopfreq = float(cutoff)
    cornerfreq = 0.4 * stopfreq

    ws = cornerfreq/nyq
    wp = stopfreq/nyq
    
    N1, wn =signal.buttord(wp, ws, 3, 40)
    b, a = signal.butter(N1, wn, btype = 'high')
    
    a2 = signal.lfilter(b, a, y) * alto2
    
    #suma de todos los filtros
    #sf = (b1 + b2 + m1 + m2 + a1 + a2) * vol
    sf = (b1 + b2 + m1 + m2 + a1 + a2)
    #graficar
    N = len(sf)
    yf = fft(sf)
    xf = np.linspace(0.0, (1.0 / (2.0 * T)),int(N / 2))
    
    plt.figure(2)
    plt.plot(xf, 2.0 / N * np.abs(yf[0:int(N / 2)]))
    plt.show()
   
###############################################################################
def APLICAR():
    #inicializacion de variables
    global Fs, b1, b2, m1, m2, a1, a2, sf, t, data, a
    
    a = 1
    #abrir archivo grabado
    rate, data = wavfile.read("primer.wav")
    #imprmir en tiempo
    t = np.linspace(0, (len(data) / rate), num = len(data))
    #graficar
    plt.figure(1)
    plt.plot(t, sf)
    plt.show()
    #tamaño a 16 bit
    scaled = np.int16(sf)
    #escribir archivo con filtro
    write(("s_filtrada.wav"), Fs, scaled)

###############################################################################
def TIEMPO():
    #inicializacion de variables
    global t, rate, data
    #abrir documento 
    rate, data = wavfile.read("primer.wav")
    #conversion a tiempo
    t = np.linspace(0, (len(data) / rate), num = len(data))
    #graficar
    plt.figure(1)
    plt.plot(t, data)
    plt.show()
    
###############################################################################
def FRECUENCIA():
    
    #abrir archivo 
    Fs, y = wavfile.read("primer.wav")
    N = len(y)
    T = 1.0 / Fs
    #x = np.linspace(0.0, N * T, N)
    #transformada de furier
    yf = fft(y)
    xf = np.linspace(0.0, (1.0 / (2.0 * T)), int(N / 2))
    yff = (2.0/N * np.abs(yf[0:N/2]))
    #graficar en frecuencia
    plt.figure(2)
    plt.plot(xf, yff)
    plt.show()
    
###############################################################################
def REPRODUCIR():
    #comparacion    
    if a == 0:
        #volumen
        rate, data = wavfile.read("primer.wav")
        #se amplifica la señal data 2 veces y se guarda en c
        c = Volumen.get() * data
        scaled = np.int16(c)
        #se graba el nuevo archivo con nombre diferente#
        wavfile.write("segundo.wav", rate, scaled)
        #abrir archivo
        rf = wave.open('segundo.wav', 'rb')
        #reproducir de a partes de 1024
        prof = rf.getsampwidth()
        channels = rf.getnchannels()
        rate = rf.getframerate()
        audioN = pyaudio.PyAudio()
        stream1  = audioN.open(format = audioN.get_format_from_width(prof), channels = channels, rate = rate, output = True)
        datos = rf.readframes(1024)
        
        while datos != b'':
            stream1.write(datos)
            datos = rf.readframes(1024)
        #cerrar
        rf.close()

            #comparcion
    if a == 1:
        
        #volumen
        rate, data = wavfile.read("s_filtrada.wav")
        #se amplifica la señal data 2 veces y se guarda en c
        c = Volumen.get() * data
        scaled = np.int16(c)
        #se graba el nuevo archivo con nombre diferente#
        wavfile.write("segundo.wav", rate, scaled)
        rf = wave.open('segundo.wav', 'rb')
    
        prof = rf.getsampwidth()
        channels = rf.getnchannels()
        rate = rf.getframerate()
        audioN = pyaudio.PyAudio()
        stream1  = audioN.open(format=audioN.get_format_from_width(prof), channels=channels, rate=rate, output=True)
        datos = rf.readframes(1024)
        
        while datos != b'':
            stream1.write(datos)
            datos = rf.readframes(1024)
        #cerrar
        rf.close()
    
###############################################################################
#creacion de ventana principal
ventana = Tk()
#tamaño
ventana.geometry("700x300+100+200")
#fondo
imagen = PhotoImage(file = "fondo.gif")
fondo = Label(ventana, image = imagen).place(x = 0, y = 0)
#titulo
ventana.title("Ecualizador")
lblusuario2 = Label(text = " ECUALIZADOR ").place(x = 270, y = 10)
a = 0
b = 0
#imagenes
Play = PhotoImage(file = "Play.gif")
#Stop = PhotoImage(file = "Pause.gif")
Grabado = PhotoImage(file = "Grabar.gif")
#botones
btnGrabar = Button(ventana, image = Grabado, command = GRABAR, font = ("Arial",14)).place(x = 30, y = 55)
btnReproducir = Button(ventana, image = Play, command = REPRODUCIR, font = ("Arial", 14)).place(x = 30, y = 125)
#btnStop = Button(ventana, image = Stop, command = STOP, font = ("Arial",14)).place(x = 30, y = 195)
btnFFT = Button(ventana, text = "FFT", command = FILTRO, font = ("Arial", 14)).place(x = 100, y = 208)
btnAplicar = Button(ventana, text = "APLICAR", command = APLICAR, font = ("Arial", 14)).place(x = 180, y = 208)
#sliders
Bajo1 = DoubleVar()
Bajo2 = DoubleVar()
Medio1 = DoubleVar()
Medio2 = DoubleVar()
Alto1 = DoubleVar()
Alto2 = DoubleVar()
Volumen = DoubleVar()
#ubicacion de slider
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Bajo1).place(x = 100, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Bajo2).place(x = 180, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Medio1).place(x = 260, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Medio2).place(x = 340, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Alto1).place(x = 420, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Alto2).place(x = 500, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 200, width = 20,from_ = 2,to = 0, resolution = 0.1, variable = Volumen).place(x = 595, y = 70)
#titulo de sliders
lblusuario2 = Label(text = " 125 Hz ").place(x = 105, y = 50)
lblusuario2 = Label(text = " 250 Hz ").place(x = 178, y = 50)
lblusuario2 = Label(text = " 500 Hz ").place(x = 258, y = 50)
lblusuario2 = Label(text = " 1000 Hz ").place(x = 332, y = 50)
lblusuario2 = Label(text = " 2000 Hz ").place(x = 412, y = 50)
lblusuario2 = Label(text = " 4000 Hz ").place(x = 504, y = 50)
lblusuario2 = Label(text = " VOLUMEN ").place(x = 584, y = 50)
#menus
# paso 1 crear la barra de menus
barramenu = Menu(ventana)
#paso 2 crear los menus
mnuarchivo = Menu(barramenu)
mnugrafica = Menu(barramenu)
#paso 3 crear los comandos de los menus
mnuarchivo.add_command(label = "Importar", command = IMPORTAR)
mnuarchivo.add_command(label = "Exportar", command = GUARDAR)
#mnuarchivo.add_separator()
mnuarchivo.add_command(label = "Salir", command = ventana.destroy)
mnugrafica.add_command(label = "Tiempo", command = TIEMPO)
mnugrafica.add_command(label = "Frecuencia", command = FRECUENCIA)
#paso 4 agergar los menus a la barra de menus
barramenu.add_cascade(label = "Archivo", menu = mnuarchivo)
barramenu.add_cascade(label = "Graficas", menu = mnugrafica)
#paso 5 indicamos que la barra de menus estara en la ventana
ventana.config(menu = barramenu)
#cerrar ventana principal
ventana.mainloop()
###############################################################################