from .models import UGChords
from .scraper import scrape_chords_for_song
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger("fetch_ug_chords")
class fetch_ug_chords() :
    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def getBaseChord(self, chord) :
        base_chords = ['C#','C','D#','Db','D','Eb','E','F#','F','G#','Gb','G','Ab','A#','A','Bb','B#','B']
        for idx, val in enumerate(base_chords):
            if (chord.startswith(base_chords[idx])):
                return base_chords[idx]
        return 'DOES NOT EXIST'

    def scrape_chords_from_ug(self, artist, song) :
        df = scrape_chords_for_song(artist, song)
        unique_chords = np.unique(df['Chords'].iloc[0])
        ugChords = UGChords(artist = df['Artist'].iloc[0], song = df['Song'].iloc[0], ug_chords = unique_chords, capo = df['Capo'].iloc[0] )
        ugChords.save()

    def getChords(self) :
        logger.error("#####################")
        logger.error(self.artist)
        logger.error(self.song)
        ugchords = UGChords.objects.filter(artist__icontains=self.artist, song__icontains=self.song)

        if not ugchords:
            #do This
            self.scrape_chords_from_ug(self.artist, self.song)
            ugchords = UGChords.objects.filter(artist__icontains=self.artist, song__icontains=self.song)

        for chords in ugchords:
            logger.error("UGCHORDS: " )
            c = chords.ug_chords.replace('[', '')
            c = c.replace(']', '')
            c = c.replace("'", '')
            logger.error(c)
            chord_list = c.split(' ')
            logger.error(chord_list)
            logger.error(chords.capo)

            if (chords.capo == 0):
                return (chord_list)

            chord_sequence = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B','C','C#','D','D#','E','F','F#','G','G#','A','A#','B','C','C#','D','D#','E','F','F#','G','G#','A','A#','B',]
            updated_chords = []
            for idx, val in enumerate(chord_list):
                chord = chord_list[idx]
                base_chord = self.getBaseChord(chord)
                rest_chord = chord.split(base_chord,1)[1]
                loc_in_chord_sequence = chord_sequence.index(base_chord)
                updated_chords.append(chord_sequence[loc_in_chord_sequence + chords.capo] + rest_chord)

            return (updated_chords)
