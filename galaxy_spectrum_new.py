#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:11:37 2020

@author: jarvis-astro
"""

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import font_manager as fm, rcParams
import mpdaf
from mpdaf import obj



'''Defining variables'''

wav = list()    #Wavelength
flux = list()   #Flux
err = list()   #1-sigma error
cont = list()  #continuum
lname_emm = list()    #emission line name
wav_emm = list()  #emission line wavelength
lname_abs = list()    #absorption line name
wav_abs = list()  #absorption line wavelength
name_sky = list()   #sky line
wav_sky = list()    #sky line wavelength



'''Importing spectrum data from the file'''

## Both method for reading the spectrum data file are working, one can either of the way mentioned
#f = open('/home/jarvis-astro/PROJECT/spectra/final_vac/G2_7_data_bin_mask_conti.txt', 'r')
#for line in f: 
#    line = line.strip()
#    columns = line.split()
#    wav_val = float(columns[0])
#    wav.append(wav_val)
#    flux_val = float(columns[1])
#    flux.append(flux_val)
#    err_val = float(columns[2])
#    err.append(err_val)
#    print("wavelength: ", wav)
#    print('flux: ', flux)
#f.close()

## OR

#a = np.genfromtxt('/home/jarvis-astro/PROJECT/spectra/final_vac/G2_7_data_bin_mask_conti.txt')     # with R=3 from mpdaf binned & masked with continuum

wav = a[:,0]
wav_a = wav
flux = a[:,1]
#print("wavelength: ", wav)
#print('flux: ', flux)
#print(wav_a)



'''Importing sky, emission and absorption lines data from the file'''

sky = open('/home/jarvis-astro/PROJECT/spectra/sky_lines.txt','r')
#print(sky.read())
#name_sky = sky[:,0]
#wav_sky = sky[:,1]
for line in sky: 
    line = line.strip('"')
    columns = line.split('"')
    name_sky_val = str(columns[0])
    name_sky.append(name_sky_val)
    wav_sky_val = float(columns[1])
    wav_sky.append(wav_sky_val)
#print('sky line name: ', name_sky)
#print('sky line wavelength: ', wav_sky)
sky.close()

emm = open('/home/jarvis-astro/PROJECT/spectra/Gal_emm_lines.txt','r')
#print('emm: ', emm.read())
for line in emm: 
    line = line.strip('"')
    #print('line: ', line)
    columns = line.split('"')
    #print('columns: ', columns)
    lname_emm_val = str(columns[0])
    #print('lname_emm_val: ', lname_emm_val)
    lname_emm.append(lname_emm_val)
    wav_emm_val = float(columns[1])
    #print('wav_emm_val: ', wav_emm_val)
    wav_emm.append(wav_emm_val)
#print('emission line name: ', lname_emm)
#print('emission line wavelength: ', wav_emm)    
emm.close()

abs = open('/home/jarvis-astro/PROJECT/spectra/Gal_abs_lines.txt','r')
for line in abs: 
    line = line.strip('"')
    columns = line.split('"')
    lname_abs_val = str(columns[0])
    lname_abs.append(lname_abs_val)
    wav_abs_val = float(columns[1])
    wav_abs.append(wav_abs_val)
#print('absorption line name: ', name_sky)
#print('absorption line wavelength: ', wav_sky)
abs.close()



'''Changing the list to numpy array'''

lname_emm = np.asarray(lname_emm,dtype=str) #Emission line name
wav_emm = np.asarray(wav_emm,dtype=float) #Wavelength of the emission line
lname_abs = np.asarray(lname_abs,dtype=str) #Absorption line name
wav_abs = np.asarray(wav_abs,dtype=float) #Wavelength of the absorption line
name_sky = np.asarray(name_sky,dtype=str) #Sky line
wav_sky = np.asarray(wav_sky,dtype=float) #Wavelength of the sky line
#print('wavelength: ', wav)
#print('flux: ', flux)
#print('sky line name: ', name_sky)
#print('sky line wavelength: ', wav_sky)
#print('emission line name: ', lname_emm) 
#print('emission line wavelength: ', wav_emm)
#print('absorption line name: ', name_sky)
#print('absorption line wavelength: ', wav_sky)



'''Converting air wavelengths to vacuum wavelengths'''

for j in range(len(wav)):
    sig = np.empty(len(wav))
    fact = np.empty(len(wav))
    #wav_v = np.empty(len(wav))
    sig[j] = (1e4 / wav[j])**2.
    fact[j] = 1.0 + (6.4328e-5 + (2.94981e-2 / (146. - sig[j])) + (2.5540e-4 / (41. - sig[j])))
    #if not isinstance(wav[j], np.ndarray):
    #    if wav[j] < 2000:
    #        fact = 1.0
    #else:
    #    ignore = np.where(wav[j] < 2000)
    #    fact[ignore] = 1.0
    #wav_v = np.empty(len(wav))
    #wav[j] = wav[j] * (1 + 6.4328e-5 + (2.94981e-2 / (146 - sig[j])) + (2.5540e-4 / (41 - sig[j])))
    wav[j] = wav[j] * fact[j]
    wav_v = wav
#print(wav_v)



'''Calculating redshift by clicking on an identified emission and absorption line'''

def redshift_emm(x):
    #b = 3727.092
    z = np.empty(len(wav_emm))
    #z = (x[0] / b[0]) - 1
    for i in range (len(wav_emm)):
        z[i] = (x[0] / wav_emm[i]) - 1
    return z   
    
def clk_emm(event):
#    global ix, iy
#    ix, iy = event.xdata, event.ydata
#    print(ix, iy)
    #x = np.empty(2, dtype=float)
    x_ip = plt.ginput(1)
    x = [x[0] for x in x_ip]
    y = [x[0] for y in x_ip]
    print("The coordinates are: ", x_ip)
    print("The x-point is: ", x)
    #print("The y-point is: ", y)
    print("Redshift is: ", redshift_emm(x))
    return redshift_emm(x)

def redshift_abs(x):
    #b = 3727.092
    z = np.empty(len(wav_abs))
    #z = (x[0] / b[0]) - 1
    for i in range (len(wav_abs)):
        z[i] = (x[0] / wav_abs[i]) - 1
    return z   
    
def clk_abs(event):
#    global ix, iy
#    ix, iy = event.xdata, event.ydata
#    print(ix, iy)
    x_ip = plt.ginput(1)
    x = [x[0] for x in x_ip]
    y = [x[0] for y in x_ip]
    print("The coordinates are: ", x_ip)
    print("The x-point is: ", x)
    print("Redshift is: ", redshift_abs(x))
    return redshift_abs(x)

    

'''Plotting the normalized spectra'''

#fig, ax  = plt.subplots()
#fig=plt.figure(1,figsize=(20,7))

plt.subplots_adjust(bottom=0.2)
f1 = plt.figure(1, figsize=(20,7), dpi=600, frameon=True)
ax = f1.add_subplot(111)

plt.rcParams['axes.unicode_minus']=False

## RomanT.tt is for Hershey fonts

fpath = os.path.join(plt.rcParams["datapath"], "/home/jarvis-astro/PROJECT/spectra/RomanT.ttf")
prop = fm.FontProperties(fname=fpath, weight='bold')
prop1 = fm.FontProperties(fname=fpath, weight='bold', size=16)
fname = os.path.split(fpath)[1]

#plt.rcParams['font.serif'] = "Times New Roman"
#plt.rcParams['font.family'] = "serif"
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
ax.set_xlabel('Observed Wavelength ($\mathregular{\AA}$)', fontproperties=prop, fontsize=20, fontweight='heavy')
ax.set_ylabel('Flux ($\mathregular{10^{-17}}$ erg s$\mathregular{^{-1}}$ cm$\mathregular{^{-2}}$ $\mathregular{\AA}\mathregular{^{-1}}$)', fontproperties=prop, fontsize=20, fontweight='heavy')
ax.axhline(y=0, color='grey', ls='--')
ax.tick_params(direction='in', which='major', length=8)
ax.tick_params(which='minor', direction='in', length=4)

ax.step(wav_v, flux*1e-3)
ax.set_xlim(5150, 5200)
#ax.set_xlim(math.floor(wav_v[0]), math.ceil(wav_v[len(wav_v)-1]))
#ax.set_xlim(math.floor(wav_v[0]), 5200)
#ax.set_ylim(math.floor(flux[0]), math.ceil(flux[len(flux)-1]))
#ax.set_ylim(-1, 1)
#ax.plot(wav, flux, drawstyle='steps-mid', c='b')  # If plotting from already given galaxy spectrum
#spec.plot() 	#If lotting from MUSE cube
#ax.plot(wav_v, err*10**17, drawstyle='steps-mid', c='b')
    
        
#cid = f1.canvas.mpl_connect('button_press_event', clk)
axcl_emm = plt.axes([0.1, 0.05, 0.2, 0.06])
clck_emm = Button(axcl_emm, 'Click here for emission line')
clck_emm.on_clicked(clk_emm)
axcl_abs = plt.axes([0.7, 0.05, 0.2, 0.06])
clck_abs = Button(axcl_abs, 'Click here for absorption line')
clck_abs.on_clicked(clk_abs)

plt.show()

