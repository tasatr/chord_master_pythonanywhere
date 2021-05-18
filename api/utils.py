from .fetch_ug_chords import fetch_ug_chords
import pandas as pd
import numpy as np
import librosa, librosa.display
from scipy.signal import stft
import os
import logging
import shutil

logger = logging.getLogger("utils")

#https://github.com/caiomiyashiro/music_and_science
COL_NAMES_NOTES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]

def calc_chromagram(x, Fs, plot=True):
    C = librosa.feature.chroma_stft(y=x, sr=Fs, tuning=0, norm=2, hop_length=1024, n_fft=4096)

    if(plot==True):
        plt.figure(figsize=(12, 3))
        plt.title('Chromagram $\mathcal{C}$')
        librosa.display.specshow(C, x_axis='time', y_axis='chroma', cmap='gray_r', hop_length=1024)
        plt.xlabel('Time (frames)'); plt.ylabel('Chroma')
        plt.colorbar(); plt.clim([0, 1])
        plt.tight_layout()
    return C

#https://github.com/caiomiyashiro/music_and_science
def chromagram_2_dataframe(chromagram, frame_duration_sec, test_version=False):
    chromagram = pd.DataFrame(np.transpose(chromagram), columns=COL_NAMES_NOTES)

    chromagram['start'] = np.arange(chromagram.shape[0]) * frame_duration_sec
    chromagram['end'] = chromagram['start'] + frame_duration_sec

    if(test_version == False):

        start_chromagram = pd.DataFrame(np.random.normal(loc=0, scale=0.01, size=chromagram.shape[1]),
                                            index=chromagram.columns).transpose()
        start_chromagram.iloc[:,-2:] = 0
        end_chromagram = pd.DataFrame(np.random.normal(loc=-1, scale=0.01, size=chromagram.shape[1]),
                                          index=chromagram.columns).transpose()
        end_chromagram.iloc[:,-2:] = chromagram.iloc[-1]['end']+.01
        chromagram = start_chromagram.append(chromagram, ignore_index=True).append(end_chromagram, ignore_index=True)

    return chromagram

#https://github.com/caiomiyashiro/music_and_science
def get_frame_stats(chromagram, signal, Fs):
    frames_per_sec = chromagram.shape[1]/(len(signal)/Fs) # Nbr of frames / length in seconds = frames per second
    frame_duration_sec = 1/frames_per_sec        # frame duration = 1 / frames per second
    return [frames_per_sec, frame_duration_sec]


#https://github.com/caiomiyashiro/music_and_science
def build_chroma_song(song_path, process_silence=True, test_version=False):

    # input data -> signal, sample frequency, chromagram and annotated dataset
    x2, Fs2 = librosa.load(song_path)
    C2 = calc_chromagram(x2, Fs2, False)
    frames_per_sec, frame_duration_sec = get_frame_stats(C2, x2, Fs2)

    pcp2 = chromagram_2_dataframe(C2, frame_duration_sec, test_version=test_version)
    return x2, Fs2, pcp2

def get_song_chromagram(song_path):
    # get predictions
    signal, sr, chromagram = build_chroma_song(song_path, process_silence=True, test_version=False)
        #TODO
        #chord_ix_predictions2 = h_markov_model.predict(chromagram[COL_NAMES_NOTES])

        #chromagram['predicted'] = get_hmm_predictions(chord_ix_predictions2, prediction_dict)
        #chromagram['predicted_cluster'] = smooth_chords_by_beat(chromagram, signal, sr, predicted_col='predicted', n_beats=1)
    return signal, sr, chromagram

#https://github.com/caiomiyashiro/music_and_science
def smooth_chords_by_beat(chromagram, signal, sr, predicted_col='predicted', n_beats=1):
    _, beats = librosa.beat.beat_track(y=signal, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    beat_times = beat_times * 2 * n_beats
    beat_times[0] = 0
    pcp = chromagram[['end', predicted_col]].copy()
    pcp['chord_cluster'] = np.digitize(pcp['end'], beat_times)
    mode_cluster = pcp.groupby('chord_cluster')[predicted_col].agg(lambda x:x.value_counts().index[0])
    pcp['predicted_cluster'] = mode_cluster.loc[pcp['chord_cluster']].values
    return pcp['predicted_cluster']

#https://github.com/caiomiyashiro/music_and_science
def simplify_predicted_chords(chromagram, predicted_col='predicted'):
    change_chord = chromagram[predicted_col] != chromagram[predicted_col].shift(-1)
    change_chord_ix = change_chord[change_chord == True].index
    filtered_pcp = chromagram.loc[change_chord_ix].copy()
    end_time_previous = np.array([0] + filtered_pcp['end'][:-1].tolist())
    filtered_pcp['start'] = end_time_previous
    # start_time_following = np.array(filtered_pcp['start'][1:].tolist())
    # start_time_following = np.append(start_time_following, filtered_pcp['end'].tail(1))
    #
    # filtered_pcp['end'] = start_time_following
    return filtered_pcp[[predicted_col, 'start', 'end']].reset_index(drop=True)

def remove_too_short_chords(chromagram, threshold, predicted_col='predicted'):
    long_chords = chromagram.end - chromagram.start > threshold
    long_chords_ix = long_chords[long_chords == True].index
    filtered_pcp = chromagram.loc[long_chords_ix].copy()
    end_time_previous = np.array([0] + filtered_pcp['end'][:-1].tolist())
    filtered_pcp['start'] = end_time_previous

    # start_time_following = np.array(filtered_pcp['start'][1:].tolist())
    # start_time_following = np.append(start_time_following, filtered_pcp['end'].tail(1))
    #
    # filtered_pcp['end'] = start_time_following
    return filtered_pcp[[predicted_col, 'start', 'end']].reset_index(drop=True)

def cleanup(directory):
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.startswith("temp")]
    for file in filtered_files:
        logger.error("################################################## REMOVING FILE %s", file)
        path_to_file = os.path.join(directory, file)
        logger.error(path_to_file)
        os.remove(path_to_file)

    try:
        shutil.rmtree('audio_output')
    except OSError as e:
        print("Error: %s : %s" % ('audio_output', e.strerror))
    return
