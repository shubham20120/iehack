#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import soundfile as sf


def feature_extraction(file_name):
    #X, sample_rate = sf.read(file_name, dtype='float32')
    X , sample_rate = librosa.load(file_name, sr=None) #Can also load file using librosa
    if X.ndim > 1:
        X = X[:,0]
    X = X.T
    
    ## stFourier Transform
    stft = np.abs(librosa.stft(X))
            
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=20).T, axis=0) #Returns N_mel coefs
    rmse = np.mean(librosa.feature.rms(y=X).T, axis=0) #RMS Energy for each Frame (Stanford's). Returns 1 value 
    spectral_flux = np.mean(librosa.onset.onset_strength(y=X, sr=sample_rate).T, axis=0) #Spectral Flux (Stanford's). Returns 1 Value
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=X).T, axis=0) #Returns 1 value
    
    #mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0) #Returns 128 values
    #chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0) #Returns 12 values
    #contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0) #Returns 7 values
    #tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0) #tonal centroid features Returns 6 values
    
    ##Return computed audio features
    return mfccs, rmse, spectral_flux, zcr


#loading the trained model
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

#feature extraction of the input audio file
audio_file = ""Avalinguo - Alan and Eduardo segment 25 - A.mp3""
mfccs, rmse, spectral_flux, zcr = feature_extraction(audio_file)

features = np.empty((0,23))
features_extract = np.hstack([mfccs, rmse, spectral_flux, zcr])
features = np.vstack([features, features_extract])

np.save('feat_testing.npy', features)
X_testing = np.load('feat_testing.npy')


#classification of the audio file
result = loaded_model.predict(X_testing)
label_dic = {
    0.0: 'Low fluency',
    1.0 : 'Medium fluency',
    2.0 : 'High fluency'
}

print(label_dic[result[0]])

