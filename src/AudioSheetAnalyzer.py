import warnings 
warnings.filterwarnings('ignore')
import argparse
from glob import glob
import pandas as pd
import os
import numpy as np
from collections import Counter
from music21 import *

from utils import xml_to_midi, get_file_name, get_file_extension
from eval import calc_accuracy,save_confusion_matrix
from utils import load_sheet_notes,load_notes,analyze_audio,get_file_path

##################### MAIN FUNCTION ###############################
def main():
    """
    This is the main function for comparing sheet music image 
    and corresponding audio recording for calculating accuracy of notes.
    """

    accuracy_list = []
    parser = argparse.ArgumentParser(description=
    "Audio Sheet Music analyzer",usage='%(prog)s [-h] [-w wavfile] [-t transfilepath] [-s sheetfilepath] [-x Musicxmlfilepath] ')

    parser.add_argument(
        "-w", "--wavfile",type = str, help="Input wavfile to be analyzed", required=False
    )    
    parser.add_argument(
        "-t", "--transfilepath",type = str, help="path of the transcribed file", required=False
    )
    parser.add_argument(
        "-s", "--sheetfilepath",type = str,metavar='\b',
        help="path of the sheet music png file", required=False
    )
    parser.add_argument(
        "-x","--musicxmlfilepath",type = str,
        help="path to store musicxml files", required=False
    )    

    args = parser.parse_args()
    output_path = os.getcwd()
    wavfile = args.wavfile
    if not wavfile:
        if args.transfilepath:
            trans_path =  args.transfilepath
        else:
            print()
            print(f'required argument missing "-t"')
            print()
            parser.print_usage()
            print()
            exit(0)
        if args.sheetfilepath:
            sheet_path = args.sheetfilepath
        else:
            print()
            print(f'Required argument missing "-s"')
            print()
            parser.print_usage()
            print()
            exit(0)

    if not args.musicxmlfilepath:
        xml_path = args.sheetfilepath
    else:
        xml_path = args.musicxmlfilepath

    if wavfile:
        analyze_audio(wavfile,get_file_path(wavfile))
        #analyze_audio(wavfile,output_path)
    else:
        d = {0:'GTruth', 1:'Transcribed'}
        skip_transcription=0
        os.chdir(trans_path)

        if os.path.exists(trans_path):
            skip_transcription = 1
        else:
            print(f'Input path f{trans_path} is invalid!!')
            print('Exiting!!')

        #read all the transcribed midi filenames
        trans_files=[i for i in os.listdir(trans_path) if i.endswith(".mid")]

        for f in trans_files:
            gtruth_arr=[]
            transcribed_arr=[]
            grtruth_dict={}
            transcribed_dict={}
            df_dict = pd.DataFrame()

            print(f'\n***** Processing {f}... ******')

            transcribed_file = os.path.join(trans_path,f)

            # find corresponding Gtruth PNG file for comparison

            search_string = os.path.join(sheet_path, '')   +  get_file_name(f).split('_')[::-1][1] + '*png'
            gtruth_file = ''
            try:
                gtruth_file = glob(search_string)[0]
                print(f'\nFound corresponding PNG file {gtruth_file}\n')
            except:
                print(f'\nPNG file corresponding to {f} not found!\n')

            # Obtain the notes list for both Ground Truth and Transcribed audio files.
            gtruth_arr = load_sheet_notes(gtruth_file,xml_path,f)
            transcribed_arr = load_notes(transcribed_file)

            if len(gtruth_arr) == 0:
                print(f'\nskipping song {f} because of OMR errors!') # there may be some errors duing OMR processing.
                continue

            # Form a dictionary out of lists
            grtruth_dict = Counter(gtruth_arr)
            transcribed_dict = Counter(transcribed_arr)

            # Form a dataframe for quick processing further.
            df_dict = pd.DataFrame([grtruth_dict,transcribed_dict]).transpose()
            df_dict.rename(columns = d, inplace = True) 

            # Calculate the accuracy score:
            acc = calc_accuracy(df_dict)
            print(f'\nNote accuracy of "{f}" and sheet image is {acc:.2f}%' )

            accuracy_list.append(acc)
            #print(f'Above save_confusion_matrix')
            save_confusion_matrix(df_dict,f,trans_path)
            #print(f'below save_confusion_matrix')


        # # Outside for loop
        print(f'Mean accuracy is {np.mean(accuracy_list):.2f}%\n')

if __name__ == "__main__":
    main()