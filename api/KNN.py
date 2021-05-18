from sklearn.neighbors import KNeighborsClassifier
from .TrainingData import TrainingData
import logging

logger = logging.getLogger("KNN")

class KNN():
    def __init__(self, ug_chords):
        training_inputs, training_outputs = TrainingData.getTrainingData(ug_chords)
        self.training_inputs = training_inputs
        self.training_outputs = training_outputs
        self.knn_classifier = KNeighborsClassifier(n_neighbors=1)
        logger.error('####################################################### in KNN init')
        logger.error(self.training_inputs)
        self.knn_classifier.fit(training_inputs, training_outputs)
        logger.error('####################################################### finished training')

    def get_classification(self, input):
        knn_predictions = self.knn_classifier.predict(input)
        return knn_predictions
