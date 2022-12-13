from array import array
from fastapi import FastAPI
from fastapi import UploadFile, File
import io
from fastapi.middleware.cors import CORSMiddleware
import numpy as np


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/row/")
def  read_root():
    return ["val1", "val2" , "val3",'val4']


@app.get("/row2/")
def  read_root(abs):
    return ["val1", "val2" ,abs]

@app.get("/search/")
def  executeSearch(parameters):
  import spotipy
  from spotipy.oauth2 import SpotifyClientCredentials
  client_id = '8d151780e7f149bbb92f1916e109eef2'
  c_secret = '3bf22a6ab36c48c0b2b7d6b1ea5985f0'
  client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=c_secret)
  sp = spotipy.Spotify(client_credentials_manager = client_credentials)

  searchResults = sp.search(q=parameters, type="track", limit = 10)
  a = searchResults.get("tracks").get("items")
  i = 0
  arrval = []
  for i in range(0,len(a)):
    s_id = a[i]['id']
    s_features = getFinalFeatures(s_id)
    arrval.append([a[i]['album']['images'][0]['url'],a[i]['artists'][0]['name'],a[i]['album']['name'],a[i]['name'],a[0]['id'],a[1]['popularity'],a[0]['album'].get("release_date")[0:4:1],s_features[0],s_features[1],s_features[2]])
  return arrval
  # Album url - Artst - Album Name - Song Name - Song Id - Popularity - Year - Energy - Instrumentalness - Tempo

@app.get("/generate_predictions/")
def run_model(input_usr):
  print("\n\n----- New Model -----\n")
  import joblib
  import numpy as np
  import pandas as pd
  import tensorflow as tf
  from tensorflow import keras
  from scipy import spatial
  import matplotlib.pyplot as plt

  # Load the saved model and datasets
  pickle_model = keras.models.load_model("ml_modelv2")
  spotify_song_data = pd.read_csv("spotify_song_data.csv")
  new_all = pd.read_csv("new_all.csv")
  input_usr = normalise_data(input_usr)
  print("input usr",input_usr)

  # Join features to user features
  training_df = new_all.copy()
  training_df['Usr_Energy'] = input_usr[0]
  training_df['Usr_Instrumentalness'] = input_usr[1]
  training_df['Usr_Popularity'] = input_usr[2]
  training_df['Usr_Tempo'] = input_usr[3]
  training_df['Usr_Year'] = input_usr[4]
  
  # Get the results of the model prediction
  final_wres = getResults(training_df,pickle_model,spotify_song_data)
  
  # - Remove non valid values instead of Looping through whole dataset 
  # - Have contingencies in case there are no songs that are too similar
  if (final_wres.shape[0] > 0):
    valid_vals = final_wres.loc[final_wres["Results"] == 9 ]
    if(valid_vals.shape[0] > 2000):
        valid_vals = valid_vals.sample(1300)
    if (valid_vals.shape[0] < 5):
      valid_vals = final_wres.loc[final_wres["Results"] >=8]
      if(valid_vals.shape[0] > 2000):
          valid_vals = valid_vals.sample(1000)
      if (valid_vals.shape[0] < 5):
        valid_vals = final_wres.loc[final_wres["Results"] >=7]
        if(valid_vals.shape[0] > 2000):
          valid_vals = valid_vals.sample(1000)
        if (valid_vals.shape[0] < 5):
          valid_vals = final_wres.loc[final_wres["Results"] >=6]
          if(valid_vals.shape[0] > 2000):
            valid_vals = valid_vals.sample(1000)
          if (valid_vals.shape[0] < 5):
            valid_vals = final_wres.loc[final_wres["Results"] >=5]
            if(valid_vals.shape[0] > 2000):
              valid_vals = valid_vals.sample(1000)
              if (valid_vals.shape[0] < 5):
                valid_vals = final_wres.loc[final_wres["Results"] >=4]
                if(valid_vals.shape[0] > 2000):
                  valid_vals = valid_vals.sample(1000)
  if valid_vals.empty:
    valid_vals = final_wres[0:2000] # in case none of them are more than 60% compatible
 
 # Utility files for final score array
  print("len of valid vals: ", valid_vals.shape[0],"\n")
  i = 0
  scores_valid_vals = []
  scores_valid_vals_arr = [0,0,0,0,0,0,0,0,0,0]
  results = 0.0 
  score_7 = 0

  # - Cosine distance to find the closest
  import numpy
  for i in range(0,len(valid_vals)):
    res_act  = [valid_vals.iloc[i][4],valid_vals.iloc[i][7],valid_vals.iloc[i][13],
                                  valid_vals.iloc[i][16],valid_vals.iloc[i][18]]
    results =  1 - spatial.distance.cosine(res_act, input_usr)
    
    if (results > 0.9):
      score_7 +=1
    if (results < 0.99):
      scores_valid_vals_arr[0] +=1
    elif (results < 0.9996):  
      scores_valid_vals_arr[1] +=1
    elif (results < 0.99996):
      scores_valid_vals_arr[2] +=1
    elif (results < 0.99999):
      scores_valid_vals_arr[3] +=1
    elif (results < 0.999996):
      scores_valid_vals_arr[4] +=1
    elif (results < 0.999999):
      scores_valid_vals_arr[5] +=1
    elif (results < 0.9999995):
      scores_valid_vals_arr[6] +=1
    elif (results < 0.9999999):
      scores_valid_vals_arr[7] +=1
    elif (results < 0.99999996):
      scores_valid_vals_arr[8] +=1
    elif (results <= 1):
      scores_valid_vals_arr[9] +=1
    scores_valid_vals.append(results)
  
  print("\nScores cosine before top10 0.9: ", score_7 )
  print("\nScores cosine distribution top10: ", scores_valid_vals_arr )
  valid_vals = valid_vals.assign(Distance_cos = scores_valid_vals)

  # Find Top 10
  # Sort the final dataframe in Descending fashion with only their id 
  final_top10 = valid_vals[['id','Distance_cos']].sort_values('Distance_cos',ascending = False).nlargest(10,'Distance_cos')
  # Use the id to get the values to return to the table
  #print(" Description of the Final Top10: ",final_top10.describe())
  final_array = []
  w = 0
  for w in range(0,5):
    final_array.append(getFinalTrackFeatures(final_top10.iloc[w][0]))
  return final_array

def getFinalFeatures(id):
  
  import spotipy
  from spotipy.oauth2 import SpotifyClientCredentials
  client_id = '8d151780e7f149bbb92f1916e109eef2'
  c_secret = '3bf22a6ab36c48c0b2b7d6b1ea5985f0'
  client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=c_secret)
  sp = spotipy.Spotify(client_credentials_manager = client_credentials)

  afeatures = sp.audio_features(tracks = id)
  tenergy = afeatures[0]['energy']
  tinstrumentalness = afeatures[0]['instrumentalness']
  #print("\n Instrumentalness: ",tinstrumentalness)
  ttempo = afeatures[0]['tempo']
  return [tenergy,tinstrumentalness,ttempo]

def getResults(training_df,pickle_model,spotify_song_data):
  pred = pickle_model.predict(training_df)
  count_index=0
  scores_res_arr = [0,0,0,0,0,0,0,0,0,0]
  results_aftermodel = []
  for i in range(0,len(pred)):
    index_max = np.argmax(pred[i])
    results_aftermodel.append(index_max)
    if (index_max <9 ):
      count_index +=1
    if (index_max == 0):
      scores_res_arr[0] +=1
    elif (index_max == 1):  
      scores_res_arr[1] +=1
    elif (index_max == 2):
      scores_res_arr[2] +=1
    elif (index_max == 3):
      scores_res_arr[3] +=1
    elif (index_max == 4):
      scores_res_arr[4] +=1
    elif (index_max == 5):
      scores_res_arr[5] +=5
    elif (index_max == 6):
      scores_res_arr[6] +=1
    elif (index_max == 7):
      scores_res_arr[7] +=1
    elif (index_max == 8):
      scores_res_arr[8] +=1
    elif (index_max == 9):
      scores_res_arr[9] +=1
  print("\nNon equal to 9", count_index)
  print("\n Distribution of predictions: ", scores_res_arr)
  final_wres = spotify_song_data.copy()
  final_wres['Results'] = results_aftermodel
  return final_wres
  
def getFinalTrackFeatures(track_id):
  import spotipy
  from spotipy.oauth2 import SpotifyClientCredentials
  client_id = '8d151780e7f149bbb92f1916e109eef2'
  c_secret = '3bf22a6ab36c48c0b2b7d6b1ea5985f0'
  client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=c_secret)
  sp = spotipy.Spotify(client_credentials_manager = client_credentials)
  searchResults = sp.track(track_id)
  album_name = searchResults['album']['name']
  artist_name = searchResults['artists'][0]['name']
  album_url = searchResults['album']['images'][0]['url']
  track_name = searchResults['name']
  
  return [album_url,track_name,artist_name,album_name]

def normalise_data(data_user):
  import pandas as pd
  from sklearn.preprocessing import LabelEncoder
  from sklearn import preprocessing
  from scipy import spatial
  
  slim_data = pd.read_csv("slim.csv")

  # Split as only one string from fetch
  data_user = data_user.split(",")
  print("\nlen_data_user",len(data_user))
  print("Data User: ",data_user)
  i = 0
  slim_dat_norm = slim_data

  # Normalise year before appending
  scl = LabelEncoder()
  slim_dat_norm['year'] = scl.fit_transform(slim_data['year'])
  print("\nslim_data length before: ",slim_data.shape[0])

  #Append new values from user
  for i in range(0,len(data_user)//5):
    new_entry = {"energy":[data_user[5*i]],"instrumentalness":[data_user[(5*i)+1]],"popularity":[data_user[(5*i)+3]]
    ,"tempo":[data_user[(5*i)+4]],"year": [data_user[(5*i)+2]]}
    new_entry_df=pd.DataFrame.from_dict(new_entry)
    print("new_entry",new_entry)
    slim_data = slim_data.append(new_entry_df,ignore_index = True)
  print("\nslim_data length after: ",slim_data.shape[0])
  slim_dat_nyr = slim_data.drop(['year'],axis=1)
  
  # Encoding all minus year
  scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
  column_names = slim_dat_nyr.columns
  mod = scaler.fit_transform(slim_dat_nyr)
  scaled_df_myr = pd.DataFrame(mod, columns=column_names)
  only_year = slim_dat_norm['year']

  # Appending the new years
  for i in range(0,len(data_user)//5):
    year_entry = {'year': [data_user[(5*i)+2]]}
    year_entry_df = pd.DataFrame.from_dict(year_entry)
    only_year = pd.concat([only_year,year_entry_df])
  
  length_opt = len(data_user)//5
  print("\nlength_opt:",length_opt)

  # Merging both normalisations
  yr = only_year['year'].tolist()
  new_all_wusr = scaled_df_myr.assign(Year=yr)
  usr_in_dat = new_all_wusr.tail(length_opt)
  #print("\n\nTAIL",new_all_wusr.tail())
  print("usr data norm", usr_in_dat)

  # Calculating Average
  averaged = [0,0,0,0,0]
  for x in range(0,length_opt):
    averaged[0] += float(usr_in_dat.iloc[x][0])
    averaged[1] += float(usr_in_dat.iloc[x][1])
    averaged[2] += float(usr_in_dat.iloc[x][2])
    averaged[3] += float(usr_in_dat.iloc[x][3])
    averaged[4] += float(usr_in_dat.iloc[x][4])
    
  averaged[0] = averaged[0]/length_opt
  averaged[1] = averaged[1]/length_opt
  averaged[2] = averaged[2]/length_opt
  averaged[3] = averaged[3]/length_opt
  averaged[4] = (averaged[4]/length_opt) - 1920
  
  return(averaged)
