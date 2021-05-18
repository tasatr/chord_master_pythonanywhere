from .models import AveragedChords
import pandas as pd
import logging
from django.db.models import Q


logger = logging.getLogger("TrainingData")


class TrainingData:
    @staticmethod
    def getTrainingData(chords):
        training_data = AveragedChords.objects.filter(Q(cleaned_chord__in=chords) | Q(cleaned_chord='<Silent>'))
        logger.error("###################################################in trainingData")
        logger.error(training_data.count())
        training_data_df = pd.DataFrame(list(training_data.values()))

        #Find missing chords
        chord_set = set(chords)
        training_chord_list = training_data_df['cleaned_chord'].tolist()
        training_chord_set = set(training_chord_list)

        missing_chords = list(sorted(chord_set - training_chord_set))
        joined_string = ",".join(missing_chords)
        logger.error("################################MISSING CHORDS: %s", joined_string)

        training_inputs = training_data_df[["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]]
        training_outputs = training_data_df.cleaned_chord

        return training_inputs, training_outputs
