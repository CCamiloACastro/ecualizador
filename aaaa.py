# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 19:59:07 2021

@author: harol
"""

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
import cv2
import numpy as np
import matplotlib.pylab as plt
import pyaudio
import scipy.io.wavfile as wavfile
import sys
import wave

from matplotlib import pyplot as plt
cap1=cv2.VideoCapture(1)
img=1
h=0
alfa=0.2
T=255
while (True):
    if (img<20):
        rec1, fondo = cap1.read()
        fondo_gris= cv2.cvtColor(fondo,cv2.COLOR_BGR2GRAY)#convierte a grises
        # Suavizado de la imagen
#        fondo_gris= cv2.GaussianBlur(fondo_gris, (21, 21), 0)
        cv2.imshow('fondo',fondo_gris)
        img=img+1
    else:
        sldbarra = Scale(ventana, orient = VERTICAL, length = 200, width = 20,from_ = 2,to = 0, resolution = 0.1, variable = Volumen).place(x = 595, y = 70)

        rec1, imagen=cap1.read()
        imagen_gris= cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)#convierte a grises
        # Suavizado de la imagen
        
        fondo_gris = imagen_gris.dot(alfa) + fondo_gris.dot(1-alfa)
        fondo_gris = fondo_gris.astype(np.uint8)
        
        cv2.imshow('fondo_2',fondo_gris)
        
        # Resta absoluta
        resta = cv2.absdiff(fondo_gris,imagen_gris)
        # Aplicamos el umbral a la imagen

        umbral = cv2.threshold(resta, 5, 255, cv2.THRESH_BINARY)[1]
        #umbral = cv2.dilate(umbral, None, iterations=2)
        
        contours,_ = cv2.findContours(umbral, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        if (contours==0):
           img=20 
        else: 
            for c in contours:
    		# Eliminamos los contornos más pequeños
        		if cv2.contourArea(c) < 2000:
        			continue
    		# Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        		(x, y, w, h) = cv2.boundingRect(c)
        		# Dibujamos el rectángulo del bounds
        		cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 0, 255), 3)
            
        cv2.imshow('final1',resta) 
        cv2.imshow('final2',umbral) 
        cv2.imshow('final3',imagen)

    if cv2.waitKey(1)  & 0xff==ord('q'):
        break
cap1.release()
cv2.destroyAllWindows()