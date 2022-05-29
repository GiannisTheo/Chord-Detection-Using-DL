import pydub
import os 
import shutil
from pydub import AudioSegment
import librosa
import numpy as np

#make a directory of all the .lab files

def get_chord_files(chord_lab_path):
    cwd = os.getcwd()
    chord_dir = os.path.join(cwd,'chord_files')
    if not os.path.isdir(chord_dir):
        os.makedirs(chord_dir)
    for root, dirs, files in os.walk(chord_lab_path):
        for file in files:
            if file.endswith(".lab"):
                shutil.copyfile(os.path.join(root,file), os.path.join(chord_dir,file))
    return 

def convert_to_wav(songs_path):
    cwd = os.getcwd()
    wav_dir = os.path.join(cwd,'songs_wav')
    if not os.path.isdir(wav_dir):
        os.makedirs(wav_dir)
    for root, dirs, files in os.walk(songs_path):
        for file in files:
            if file.endswith('.mp3'):
                track = AudioSegment.from_file(os.path.join(root,file),format='mp3')
                waveform = track.export(os.path.join(cwd,wav_dir,file[:-3]+'wav'),format = 'wav')
                print('exported one wav file')
            elif file.endswith('.m4a'):
                track = AudioSegment.from_file(os.path.join(root,file),format='m4a')
                waveform = track.export(os.path.join(cwd,wav_dir,file[:-3]+'wav'),format = 'wav')
                print('exported one wav file')
    return

def make_stft_dataset(songs_path):
    cwd = os.getcwd()
    stft_dir = os.path.join(cwd,'stft_dataset')
    if not os.path.isdir(stft_dir):
        os.makedirs(stft_dir)
    for file in os.listdir(songs_path):
        waveform,sr = librosa.load(os.path.join(songs_path,file))
        stft = librosa.stft(waveform)
        stft_mag = np.abs(stft)
        np.save(os.path.join(stft_dir,file[:-4]),stft_mag)
        print("Saved {file_name} stft".format(file_name = file[:-4]))
    return 



if __name__ == '__main__':
    #get_chord_files('chordlab')
    #convert_to_wav('songs')
    make_stft_dataset('songs_wav')

