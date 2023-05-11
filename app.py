import os.path
import random
import streamlit as st
import pandas as pd
import random

m3u_filepaths_file = 'playlists/streamlit.m3u8'
FEATURES_PATH = 'CSV/features3.csv'
STYLES_PATH="CSV/styles.txt"
AUDIO_PATHS="CSV/audio_paths1.csv"


def styles():
    with open(STYLES_PATH, "r") as file:
        styles = file.read().splitlines()
    return styles

def load_essentia_analysis():
    return pd.read_csv(FEATURES_PATH)

def load_paths():
    doc=pd.read_csv(AUDIO_PATHS)
    audio_paths=doc['audio paths'].tolist()

    return audio_paths

def audio_path_treatment(audio_paths):
    new_path_list=[]
    for path in audio_paths:
        new_path=path.replace('/audio_chunks/',"/audio/")
        #print(new_path)
        directories = new_path.split('/')
        audio_index = directories.index('audio')
        new_path = '/'.join(directories[audio_index:])
        new_path_list.append(new_path)

    return new_path_list


st.write('# Playlist creator. Santiago Diana')
st.write('Using audio features extracted from `Essentia`')
audio_analysis = load_essentia_analysis()
audio_analysis_styles = audio_analysis['predominant music style'].tolist()  ## Styles of our data. 
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('## 🔍 Select')
st.write('### By style')
st.write('Features statistics:')
st.write(audio_analysis.describe())

styles_list=styles()

style_select = st.multiselect('Select which style you want to know more about:', styles_list) ## Here I have to show all 400 and see if there is any that has been activated. 

if style_select:
    
    style_select=', '.join(style_select)
  
    if style_select in audio_analysis_styles:
        count= audio_analysis_styles.count(style_select)
        st.write(f'The style "{style_select}" appears "{count}" times in this dataset')
    else:
        
        st.write(f'There is no song with "{style_select}" style as predominant ')

path="audio"
audio_paths=load_paths()

ranges=['Below 70','Between 70 and 100','Between 100 and 130', 'More than 130']
bpms=audio_analysis['bpm'].tolist()
st.write('## BPM')
bpm_selector = st.multiselect('Select a range of BPM for your desired song:', ranges)

minus70_indexes=[]
bt_70_100_indexes=[]
bt_100_130_indexes=[]
more130_indexes=[]

for i,bpm in enumerate(bpms):
        if bpm<70:
            minus70_indexes.append(i)
        elif bpm>70 and bpm<100:
            bt_70_100_indexes.append(i)
        elif bpm>100 and bpm<130:
            bt_100_130_indexes.append(i)
        elif bpm>130:
            more130_indexes.append(i)

if bpm_selector: 
    
    if bpm_selector == ['Below 70']:
        selection= random.sample(minus70_indexes, 10)
        values_list=[]
        for index in selection:
            value = audio_paths[index]
            values_list.append(value)
        st.write(f'10 audio files that contain that value of bpm are: "{values_list}"')

    elif bpm_selector == ['Between 70 and 100']:
        selection= random.sample(bt_70_100_indexes, 10)
        values_list=[]
        for index in selection:
            value = audio_paths[index]
            values_list.append(value)
        st.write(f'10 audio files that contain that value of bpm are: "{values_list}"')

    elif bpm_selector == ['Between 100 and 130']:
        selection= random.sample(bt_100_130_indexes, 10)
        values_list=[]
        for index in selection:
            value = audio_paths[index]
            values_list.append(value)
        st.write(f'10 audio files that contain that value of bpm are: "{values_list}"')

    elif bpm_selector == ['More than 130']:
        selection= random.sample(more130_indexes, 10)
        values_list=[]
        for index in selection:
            value = audio_paths[index]
            values_list.append(value)
        st.write(f'10 audio files that contain that value of bpm are: "{values_list}"')
    
    if len(values_list)<10:
        st.write("There are less than 10 audios in this dataset that fit that option")
    else:
        for audio in values_list:
            audio_file=open(audio,"rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')




### DANCEABILITY. Let's put an slider. 

st.write('## Danceability')

danceability=audio_analysis['danceability'].tolist()
danceability = [num * 10 for num in danceability]

slid=st.slider('Danceability',min_value=0,max_value=10,value=0,step=1)
butt=st.button('Analyze by danceability')  


if butt:
    possible_audios_indexes=[]
    values_list2=[]

    for i,dance in enumerate(danceability):
        if dance>slid:
            possible_audios_indexes.append(i)

    selection= random.sample(possible_audios_indexes, 10)
    for index in selection:
        value = audio_paths[index]
        values_list2.append(value)
 
    st.write(f'10 audio files that their danceability value is bigger than the one selected: "{values_list2}"')
    st.write(f'The "{len(possible_audios_indexes)/len(danceability)*100}"% of the audios in the dataset have more danceability value than the one selected in the slider')

    
    if len(values_list2)<10:
        st.write("There are less than 10 audios in this dataset that fit that option")
    else:
        for audio in values_list2:
            audio_file=open(audio,"rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')


### Voice or instrumental.

st.write('## VOICE OR INSTRUMENTAL')
st.write('### Voice')
st.write('If you move upper you will get a voiced song')

slid2=st.slider('Voice',min_value=0,max_value=10,value=0,step=1)
butt2=st.button('Give me some songs')  

voices=audio_analysis['voice'].tolist()
voices = [num * 10 for num in voices]


if butt2:
    possible_audios_indexes2=[]
    values_list3=[]

    for i,voice in enumerate(voices):
        if voice>slid2:
            possible_audios_indexes2.append(i)

    selection= random.sample(possible_audios_indexes2, 10)
    for index in selection:
        value = audio_paths[index]
        values_list3.append(value)

    st.write(f'10 audio files that their activation related to voice is higher than the value in the slider: "{values_list3}"')
    st.write(f'The "{len(possible_audios_indexes2)/len(voices)*100}"% of the audios in the dataset have more "voiced" value than the one selected in the slider')

    if len(values_list3)<10:
        st.write("There are less than 10 audios in this dataset that fit that option")
    else:
        for audio in values_list3:
            audio_file=open(audio,"rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')


## Arousal and valence. 

st.write('## AROUSAL AND VALENCE')
st.write('Select a value for arousal and a value for valence')

slid3=st.slider('Arousal',min_value=2,max_value=5,value=0,step=1)
slid4=st.slider('Valence',min_value=2,max_value=7,value=0,step=1)
butt3=st.button('Give me some songs with this arousal/valence distribution')

arousals=audio_analysis['arousal'].tolist()
valences=audio_analysis['valence'].tolist()

if butt3:
    possible_audios_indexes3=[]
    values_list4=[]

    for i,(arousal,valence) in enumerate(zip(arousals,valences)):
        if arousal>slid3 and valence>slid4:
            possible_audios_indexes3.append(i)

    selection= random.sample(possible_audios_indexes3, 10)

    for index in selection:
        value = audio_paths[index]
        values_list4.append(value)

    
    st.write(f'10 audio files that their activation related to arousal/valence is higher than the values in the sliders: "{values_list4}"')
    st.write(f'The "{len(possible_audios_indexes3)/len(arousals)*100}"% of the audios in the dataset have more arousal/valence value than the ones selected in the sliders')

    if len(values_list4)<10:
        st.write("There are less than 10 audios in this dataset that fit that option")
    else:
        for audio in values_list4:
            audio_file=open(audio,"rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')


st.write('## PLAYLIST GENERATOR')
butt_RUN=st.button('Give me 10 songs with all the combinations regarding Danceability, Voice/Instrumental and Arousal/Valence')

if butt_RUN:
    
    possible_audios_indexes4=[]
    values_list5=[]

    for i,(bpm,dance,voice,arousal,valence) in enumerate(zip(bpms,danceability,voices,arousals,valences)):
        if dance>slid and voice>slid2 and arousal>slid3 and valence>slid4:
            possible_audios_indexes4.append(i)
    
    if len(possible_audios_indexes4)>10:
        selection= random.sample(possible_audios_indexes4, 10)

        for index in selection:
            value = audio_paths[index]
            values_list5.append(value)

        st.write(f'10 audio files that their activation related to arousal/valence is higher than the values in the sliders: "{values_list5}"')
        st.write(f'There are "{len(possible_audios_indexes4)}" audios that fit every condition you mentioned above')

    if len(values_list5)<10:
        st.write("There are less than 10 audios in this dataset that fit that option")
    else:
        for audio in values_list5:
            audio_file=open(audio,"rb")
            audio_bytes=audio_file.read()
            st.audio(audio_bytes,format='audio/mp3')
