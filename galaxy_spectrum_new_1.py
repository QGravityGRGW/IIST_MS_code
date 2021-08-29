#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 01:06:44 2020

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
#import galaxy_spectrum as gs



'''Extracting Cube and subcube from MPDAF'''

#cube = obj.Cube('/home/jarvis-astro/PROJECT/MUSE Data/ADP.2017-03-24T13:24:09.696.fits')
#ra = obj.hms2deg('02:09:31.351')  #Enter RA in hours, minutes and seconds
#dec = obj.dms2deg('-04:38:40.00') #Enter DEC in degress, minutes and seconds
#size = 10 #Enter circular radius
#sub = cube.subcube((dec,ra), size)
#img = sub.sum(axis=0)
#spec = sub.sum(axis=(1,2))



'''Defining variables'''
#0.39047	# absorber redshift
wav = list()    #Wavelength
flux = list()   #Flux
err = list()   #1-sigma error
cont = list()  #continuum
z = 0.38954 #Redshift of the galaxy (Change here!!!!!!)
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



'''Redshifting the wav_emm and wav_abs'''

for i in range(len(wav_emm)):
    wav_emm[i] = wav_emm[i] * (1 + z)
    
for i in range(len(wav_abs)):
    wav_abs[i] = wav_abs[i] * (1 + z)

    

'''Plotting the normalized spectra'''
#fig, ax  = plt.subplots()
#fig=plt.figure(1,figsize=(20,7))

plt.subplots_adjust(bottom=0.12, top=0.78)
f1 = plt.figure(1, figsize=(20,7), dpi=600, frameon=True)
ax = f1.add_subplot(111)

plt.rcParams['axes.unicode_minus']=False

#RomanT.tt is for Hershey fonts
fpath = os.path.join(plt.rcParams["datapath"], "/home/jarvis-astro/PROJECT/spectra/RomanT.ttf")
prop = fm.FontProperties(fname=fpath,weight='bold')
prop1 = fm.FontProperties(fname=fpath,weight='bold',size=16)
fname = os.path.split(fpath)[1]

#plt.rcParams['font.serif'] = "Times New Roman"
#plt.rcParams['font.family'] = "serif"
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
ax.set_xlabel('Observed Wavelength ($\mathregular{\AA}$)',fontproperties=prop,fontsize=20,fontweight='heavy')
ax.set_ylabel('Flux ($\mathregular{10^{-17}}$ erg s$\mathregular{^{-1}}$ cm$\mathregular{^{-2}}$ $\mathregular{\AA}\mathregular{^{-1}}$)', fontproperties=prop,fontsize=20,fontweight='heavy')
ax.axhline(y=0,color='grey',ls='--')
ax.tick_params(direction='in', which='major', length=8)
ax.tick_params(which='minor', direction='in', length=4)


ax.set_xlim(math.floor(wav_v[0]), math.ceil(wav_v[len(wav_v)-1]))
#ax.set_xlim(math.floor(wav_v[0]), 5000)
#ax.set_xlim(4900, 5100)
#ax.set_xlim(8600,math.ceil(wav_v[len(wav_v)-1]))
#ax.set_ylim(math.floor(flux[0]), math.ceil(flux[len(flux)-1]))
ax.set_ylim(-1.5, 1.5)

for label in ax.get_xticklabels():
    label.set_fontproperties(prop)
    label.set_fontsize(16)
        
for label in ax.get_yticklabels():
    label.set_fontproperties(prop)    
    label.set_fontsize(16)
    #label = plt.axes(yscale='log')
ax.minorticks_on()

ax.step(wav_v, flux*1e-3)
#ax.plot(wav_v, flux, drawstyle='steps-mid', c='b')  	# If plotting from already given galaxy spectrum
#spec.plot() 	# If lotting from MUSE cube
#ax.plot(wav_v,err*10**17,drawstyle='steps-mid',c='b')



'''Making tick marks for different lines in the spectrum'''

for i in range((len(wav_emm))):
    if wav_emm[i] <= wav_v[len(wav_v)-1] and wav_emm[i]>=wav_v[0]:
        ax.vlines(wav_emm[i],0.7,0.8,colors='m')
        ax.text(wav_emm[i],0.82,s=lname_emm[i],fontsize=9,rotation='vertical',fontproperties=prop,fontweight='heavy')
for j in range((len(wav_abs))):
    if wav_abs[j]<=wav_v[len(wav_v)-1] and wav_abs[j]>=wav_v[0]:
        ax.vlines(wav_abs[j],-0.2,-0.1,colors='orange')
        ax.text(wav_abs[j],-0.53,s=lname_abs[j],fontsize=9,rotation='vertical',fontproperties=prop,fontweight='heavy')
for k in range((len(wav_sky))):
    if wav_sky[k] <= wav_v[len(wav_v)-1] and wav_sky[k]>=wav_v[0]:
        ax.vlines(wav_sky[k],3.5,3.8,colors='c')
        ax.text(wav_sky[k],4.0,s=name_sky[k],fontsize=9,rotation='vertical',fontproperties=prop,fontweight='heavy')
ax.text(7100, 1.0,s='G1 \nVLT/MUSE',fontproperties=prop,fontsize=14,fontweight='heavy',color='g')
ax.text(7100, 0.86,s='$\mathregular{z_{gal}=0.38954}$',fontproperties=prop,fontweight='heavy',fontsize=14,color='g')
##plt.savefig('G3_mod1.png')



'''For moving forward and backward to see if all the lines are fitted correctly'''

b = int(input("Enter width: "))

def next(event):
    x = ax.get_xlim()
    ax.set_xlim(x[0]+b,x[1]+b)
##    print('next')
    plt.draw()
    
def prev(event):
    x = ax.get_xlim()
    ax.set_xlim(x[0]-b,x[1]-b)
##    print('prev')
    plt.draw()
    
axprev = plt.axes([0.7, 0.01, 0.08, 0.05])
axnext = plt.axes([0.8, 0.01, 0.08, 0.05])
bnext = Button(axnext, 'Next')
bnext.on_clicked(next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(prev)



plt.show()
