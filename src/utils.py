import music21 as m12
import pretty_midi
from glob import glob
import subprocess
import os
import seaborn as sns              # data visualization based on matplotlib
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scalefinder import Tonal_Fragment

def load_sheet_notes(f,dest_dir,filename):
  """
  This function extracts the notes list from a sheet image using OEMER tool and music21 library.

  :param f: PNG file for which pitch information is to be obtained. 
  :param dest_dir: The directory where temporary music xml file gets saved.
  :param filename: Name of the file without path.

  :return: List of notes.
  """  
  gtruth_notes = []

  try:
    args =  " -o " + (os.path.join(dest_dir)).strip() + " " + (os.path.join(f)).strip() + ' --save-cache'
    subprocess.run(['Oemer', '-o', (os.path.join(dest_dir)).strip(), (os.path.join(f)).strip(), '--save-cache'])
  except:
    return [] 

  search_string = os.path.join(dest_dir, '')   +  get_file_name(filename).split('_')[::-1][1] + '*musicxml'
  gtruth_file = glob(search_string)[0]
  return(xml_to_midi(gtruth_file,dest_dir))



def load_notes(filename_midi):
  """
  This function extracts the MIDI notes/pitch information.

  :param file: MIDI file for which pitch information is to be obtained. 
  :return: List of notes.
  """    
  notes=[]
  midi_data = pretty_midi.PrettyMIDI(filename_midi)
  for instrument in midi_data.instruments:
    if not instrument.is_drum:
      for note in instrument.notes:
        notes.append(str(pretty_midi.note_number_to_name(note.pitch)))
  return notes

def xml_to_midi(fn,dest_dir):
  """
  This function converts a xml file to MIDI and then extracts notes using music21

  :param fn: XML file for which pitch information is to be obtained. 
  :param dest_dir: Directory where temporary MIDI file will be put. 

  :return: List of notes.
  """   
  xml_data = m12.converter.parse(fn)
  c = m12.converter.parse(fn)
  c.write('midi',fp=os.path.join(dest_dir,'a.mid'))
  notes = load_notes(os.path.join(dest_dir,'a.mid'))
  return notes

def get_file_name(link):
    """
    This function splits the filename and returns name without extension

    :param file: full filename with extension

    :return: filename without extension
    """     
    newPath = link.replace(os.sep, '/')
    filename = newPath.split('/')[::-1][0]
    return (filename.split('.')[::-1][1])

def get_file_extension(link):
    """
    This function splits the filename and returns extension without the name

    :param file: full filename with extension

    :return: extension without filename
    """     
    filename = link.split('/')[::-1][0]
    return filename.split('.')[::-1][0]

def get_file_path(link):
    """
    This function splits the filename and returns path without the name

    :param file: full filename with extension

    :return: path without filename
    """     

    return os.path.dirname(link)


def analyze_audio(wavfile,save_path):

  # Get the beat graph
  y, sr = librosa.load(wavfile)
  y_harmonic, y_percussive = librosa.effects.hpss(y)

  tempo, beat_frames = librosa.beat.beat_track(y=y_harmonic, sr=sr)

  print('\nDetected Tempo: '+ str(round(tempo,0)) + ' beats/min')
  beat_times = librosa.frames_to_time(beat_frames, sr=sr)
  beat_time_diff = np.ediff1d(beat_times)
  beat_nums = np.arange(1, np.size(beat_times))

  fig, ax = plt.subplots()
  fig.set_size_inches(15, 5)
  ax.set_ylabel("Time difference (s)")
  ax.set_xlabel("Beats")
  g = sns.barplot(beat_nums, beat_time_diff, palette="rocket",ax=ax)
  g = g.set(xticklabels=[])
  #file_string = os.path.basename(wavfile)[1] + '_Beatgraph.png'
  print(f'wavfile path is {wavfile}')
  file_string = get_file_name(wavfile) + '_Beatgraph.png'
  graph_path = os.path.join(save_path,file_string)
  plt.savefig(graph_path)
  print(f'\nBeat graph file saved at {graph_path}\n')

  # Get the chromogram
  hop_length = 512
  chromagram = librosa.feature.chroma_stft(y, sr=sr, hop_length=hop_length)
  fig, ax = plt.subplots(figsize=(15, 3))
  img = librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
  fig.colorbar(img, ax=ax)
  file_string = get_file_name(wavfile) + '_Chromagraph.png'
  graph_path = os.path.join(save_path,file_string)
  plt.savefig(graph_path)
  print(f'Chroma graph file saved at {graph_path}\n')  

  # Get the 'key' of the piano song
  y_harmonic, y_percussive = librosa.effects.hpss(y)
  tf = Tonal_Fragment(y_harmonic, sr, tend=22)
  tf.print_key()

