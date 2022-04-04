# music-moderation-
This repository contains all the code developed for the **Music Moderation** track as part of the fellowship cohort of Jan-Apr 2022.

The project aims to analyze an end user's piano performance by  :
 1. Matching the notes played against the corresponding sheet music image file.
 2. Extracting and plotting various features like 'Pitch','Velocity','Tempo' from the audio file.

# Table of Contents
  * [Setup and Requirements](#installation)
  * [Working Pipeline](#pipeline)
  * [Tutorials](#tutorials)
  * [Dataset](#dataset)
  * [Usage](#usage)


# Setup and Requirements <a id="installation"></a>
For a list of required python packages see the *requirements.txt*
or just install them all at once using pip.
```
pip install -r requirements.txt
```

# Pipeline <a id="pipeline"></a>
![image](https://user-images.githubusercontent.com/93938450/158359692-7162ae00-f7d7-484f-b568-9b12ed8cc2ff.png)

The above diagram captures the main steps and the flow of the process:
1. **Automatic Music Transcription (AMT)** - We make use of google's magenta transformer. More information at https://magenta.tensorflow.org/transcription-with-transformers

2. **Optical Music Recognition (OMR)** - We make use of an existing open source repo - https://github.com/BreezeWhite/oemer
3. **music21 Libary** - A Python-based toolkit for computer-aided musicology. More info at : https://web.mit.edu/music21/


# Dataset <a id="dataset"></a>
Dataset from [flowkey](https://www.flowkey.com/en) website was scraped using a utility at https://github.com/MatthiasLienhard/flowkey_dl

Dataset is located at [link](https://drive.google.com/drive/folders/15L8ZF9TECMFo_n6azNUGpDAmfRN141kJ?usp=sharing) and contains around 65 piano performances in form of:
- 'Raw wav files'.
- Corresponding 'sheet image PNG files'.

The dataset only contains Intermdediate, Advanced & Pro level songs.

The dataset can be downloaded like below:

1. !pip install --upgrade --no-cache-dir gdown

2. %cd /content/gdrive/MyDrive/BaselineExperiments

3. !gdown --id 1V4tZryiQgTUjgUSGhhvqd62BYaE9qaj4   

4. !unzip BaselineDataset-20220222T143509Z-001.zip

**Please note** : While scraping data from flowkey, video recordings of songs were converted to 'wav' format using an online tool.

# Tutorials
If you want to just get familiar with the underlying functions & concepts, check out or tutorials. So far we provide the following tutorials as ipython notebooks:

1. Librosa_STFT_Intro
2. AccuracyConfusionMatrix Tutorial
3. SystematicAnomalyAddition&Detection Tutorial
4. Compare images Tutorial
5. Embedding Tutorial 

# Usage
There are 2 modes to run the script:

### <ins>**1) Note accuracy comparison b/w Audio recording & corresponding sheet Image**</ins>

First, transcribe the raw audio file using notebook [**"MagentaTranscription.ipynb"**](src/MagentaTranscription.ipynb)

Then, run the following command to execute the script and compare the Sheet Image PNG file and transcribed MIDI (obtained above).

**python .\AudioSheetAnalyzer.py -t "C:\transcribedFiles" -x "C:\xmlFiles" -s "C:\sheetimageFiles"**

It takes 2 mandatory parameters as input:
1. -t (transfilepath) i.e directory where transcribed files are located.
2. -s (sheetfilepath) i.e. directory where sheet image files are located.

Following parameter is optional:

3. -x (xmlfilepath) i.e. directory where to generate intermediate musicxml file.

**Sample Output**

![image](https://user-images.githubusercontent.com/93938450/158544413-52934be2-2733-4a13-ba5d-4bd8a102b24d.png)

### <ins>**2) Audio recording analysis**</ins>

One can pass raw audio recording of piano music in form of 'wav' file and the script finds out the following:

i. Beat Analysis - Approximation of tempo as well as the beat onset indices.

ii. Chromagram - Consists of 12 bins representing the 12 distinct semitones (or chroma) of the musical octave. 

iii. Key finder - Analyzes the key that a song is in, i.e. F major or C# minor, using the **Krumhansl-Schmuckler key-finding** algorithm.

iv. Velocity plot - Uses [auboio](https://aubio.org/) library to plot velocity graph. The key velocity is an integer between 0 and 127, which depicts the intensity of the sound


**Sample Output**

![image](https://user-images.githubusercontent.com/93938450/158544221-acef000e-8e3e-4649-aba8-7a42571660d7.png)

**Beatgraph**
![image](https://user-images.githubusercontent.com/93938450/158540805-f1f48ec6-7788-46f0-a721-a527f1a485b8.png)

**Chromagram**
![image](https://user-images.githubusercontent.com/93938450/158540862-a4aaf2ef-7ed9-468d-8481-b5b225804ba6.png)

**Velocity plot**
![image](https://user-images.githubusercontent.com/93938450/160083313-35381002-6d57-47a1-a0f5-31cba1933e44.png)











