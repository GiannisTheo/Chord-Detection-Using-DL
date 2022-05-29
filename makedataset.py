import pandas as pd
import librosa
import os
import numpy as np
import pickle


def get_all_chords(chord_dir):
  unique_chords = set()
  for file in os.listdir(chord_dir):
    path = os.path.join(chord_dir,file)
    contents = pd.read_csv(path,delim_whitespace=True)
    chords = contents.iloc[:,2].values

    for chord in chords: 
      unique_chords.add(chord)
  return unique_chords

def assign_index_to_chords(chords):
  mapping = dict()
  for i,c in enumerate(chords):
    mapping[c] = i
  with open('chord_idxs.pkl', 'wb') as f:
    pickle.dump(mapping, f)
  return 

def make_onset_labels(labels_path,chords_set):
  all_labels = []
  for file in os.listdir(labels_path):
    path = os.path.join(labels_path,file)
    contents = pd.read_csv(path,delim_whitespace=True)
    finish_time = contents.values[-1,1]
    time_frames = librosa.time_to_frames(finish_time)
    contents = contents.iloc[:,[0,2]].values
    onset_labels = np.zeros((len(chords_set),time_frames))
    for content in contents:
      onset_labels[chords_set[content[1]],librosa.time_to_frames(content[0])] = 1
    all_labels.append(onset_labels)
  return all_labels


def make_frame_labels(labels_path,chords_set):
  all_labels = []
  for file in os.listdir(labels_path):
    path = os.path.join(labels_path,file)
    contents = pd.read_csv(path,delim_whitespace=True).values
    finish_time = contents[-1,1]
    time_frames = librosa.time_to_frames(finish_time)
    onset_labels = np.zeros((len(chords_set),time_frames))
    for content in contents:
      start_frame = librosa.time_to_frames(content[0])
      end_frame = librosa.time_to_frames(content[1])
      onset_labels[chords_set[content[2]],start_frame:end_frame+1] = 1
    all_labels.append(onset_labels)
  return all_labels

def get_sample_from_song(sec,song, chords):
  #print('song dimensions are ',song.shape)
  time_frames = librosa.time_to_frames(sec)
  #print('time frames corresponding to sec ',time_frames)
  start = random.randint(0,song.shape[1]-time_frames)
  #print('print starting frame to sample ',start)
  sample_x = song[:,start:start+time_frames]
  sample_y = chords[:,start:start+time_frames]
  return sample_x,sample_y

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
  cwd = os.getcwd()
  #for file in os.listdir('songs_wav'):
    #waveform,sr = librosa.load(os.path.join(cwd,'songs_wav',file))
    #stft = librosa.stft(waveform,)
    #print('no error with wav file')
  # assign_index_to_chords(get_all_chords('chord_files'))
  # with open('chord_idxs.pkl', 'rb') as f:
  #   loaded_dict = pickle.load(f)
  # print(loaded_dict)