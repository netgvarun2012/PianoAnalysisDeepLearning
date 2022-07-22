from sklearn.metrics import accuracy_score
import os

def calc_accuracy(df_dict):
  """
  This function calculates the accuracy score for a dataframe of notes passed.

  :param file: Dataframe containing Gtruth and Transcribed notes.
  :return: The accuracy score.
  """    
  list_gtruth=[]
  list_transcribed=[]

  for i in df_dict.index:
    if (df_dict['Transcribed'][i].astype(int) > df_dict['GTruth'][i].astype(int)):
      for j in range(df_dict['Transcribed'][i].astype(int)):
        list_transcribed.append(i)
        if(j < df_dict['GTruth'][i].astype(int)):
          list_gtruth.append(i)
        else:
          list_gtruth.append('NL')
    else:
      for k in range(df_dict['GTruth'][i].astype(int)):
        list_gtruth.append(i)
        if(k < df_dict['Transcribed'][i].astype(int)):
          list_transcribed.append(i)
        else:
          list_transcribed.append('NL')

  return (accuracy_score(list_gtruth , list_transcribed)*100)

def save_confusion_matrix(df_dict,filename,savepath):
  """
  This function calculates displays the confusion matrix out of dataframe passed.

  :param df_dict : Dataframe containing Gtruth and Transcribed notes.
  :param filename : Filename with which to save the Confusion matrix.

  :return : None
  """
  from sklearn.metrics import confusion_matrix
  from sklearn.utils.multiclass import unique_labels
  import seaborn as sns
  import matplotlib.pyplot as plt

  list_gtruth=[]
  list_transcribed=[]

  for i in df_dict.index:
    if (df_dict['Transcribed'][i].astype(int) > df_dict['GTruth'][i].astype(int)):
      for j in range(df_dict['Transcribed'][i].astype(int)):
        list_transcribed.append(i)
        if(j < df_dict['GTruth'][i].astype(int)):
          list_gtruth.append(i)
        else:
          list_gtruth.append('NL')
    else:
      for k in range(df_dict['GTruth'][i].astype(int)):
        list_gtruth.append(i)
        if(k < df_dict['Transcribed'][i].astype(int)):
          list_transcribed.append(i)
        else:
          list_transcribed.append('NL')

  labels_plot = unique_labels(list_gtruth, list_transcribed)
  cf_matrix = confusion_matrix(list_gtruth,list_transcribed,labels=labels_plot)

  fig, ax = plt.subplots(figsize=(11,11))         # Sample figsize in inches
  ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

  ax.set_title('Seaborn Confusion Matrix with labels\n\n');
  ax.set_xlabel('\nPredicted Notes')
  ax.set_ylabel('Actual Notes ');


  ax.xaxis.set_ticklabels(labels_plot)
  ax.yaxis.set_ticklabels(labels_plot)


  ## Display the visualization of the Confusion Matrix.
  #plt.show()
  file_string = filename + 'cMatrix.png'

  graph_path = os.path.join(savepath,filename)
  plt.savefig(graph_path)
  print(f'\nConfusion matrix file saved at {graph_path}\n')