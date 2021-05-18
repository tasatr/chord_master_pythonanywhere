from rest_framework import serializers
from .models import Video, UGChords, ChromaToChord, AveragedChords

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id', 'title', 'artist', 'song', 'chords', 'result_video', 'created_date')

class CreateVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('video_id', 'title', 'artist', 'song')

class UGChordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGChords
        fields = ('id', 'artist', 'song', 'ug_chords', 'capo')

class ChromaToChordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChromaToChord
        fields = ('id','C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B', 'chord', 'cleaned_chord')

class AveragedChordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AveragedChords
        fields = ('id','C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B', 'cleaned_chord', 'count')
