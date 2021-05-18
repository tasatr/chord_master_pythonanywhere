from django.shortcuts import render
from django.core.files import File
from rest_framework import generics, status
from .serializers import VideoSerializer, CreateVideoSerializer, UGChordSerializer, ChromaToChordSerializer, AveragedChordsSerializer
from .models import Video
from .models import UGChords, ChromaToChord, AveragedChords
from rest_framework.views import APIView
from rest_framework.response import Response
from .fetch_ug_chords import fetch_ug_chords
from .utils import get_song_chromagram, COL_NAMES_NOTES, smooth_chords_by_beat, simplify_predicted_chords, remove_too_short_chords, cleanup
from .subtitles import create_subtitles, burn_subtitles_to_video
from .KNN import KNN
from .Download import Download
import logging
import csv

# Create your views here.

logger = logging.getLogger("Views")

class VideoView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class CreateVideoView(APIView):
    logger.error('Goodbye, cruel world!')
    serializer_class = CreateVideoSerializer

    def post(self, request, format=None):
        logger.error('#####Inside post, request data: ')
        logger.error(request.data)

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        #TODO: Remove this
        #Video.objects.all().delete()

        result = cleanup('.')

        video = Video.objects.filter(video_id = serializer.initial_data.get('video_id')).first()
        logger.error('##############################Past queryset')
        logger.error(video)
        if video:
            logger.error("#################VIDEO EXISTS")
            logger.error(video.result_video)

            return Response(VideoSerializer(video).data, status=status.HTTP_200_OK)

        if serializer.is_valid():
            logger.error('serializer is valid')
            video_id = serializer.data.get('video_id')
            logger.error('video_id is ')
            logger.error(video_id)
            title = serializer.data.get('title')
            artist = serializer.data.get('artist')
            song = serializer.data.get('song')

            #Download the video and audio
            audio = Download.download_mp3(video_id)
            video = Download.download_video(video_id)

            #Extract background
            finished = Download.separate_vocal()

            #Get chords for this song from Ultimate Guitar
            ugChordsClass = fetch_ug_chords(artist, song);
            ugChords = ugChordsClass.getChords();

            #Get the generated chord sequence for this song
            signal, sr, chromagram = get_song_chromagram('audio_output/temp/accompaniment.wav')

            #Get predictions
            knn = KNN(ugChords)
            predictions = knn.get_classification(chromagram[COL_NAMES_NOTES])

            chromagram['predicted'] = predictions
            chromagram['predicted_cluster'] = smooth_chords_by_beat(chromagram, signal, sr, predicted_col='predicted', n_beats=1)
            chords_simplified = simplify_predicted_chords(chromagram)
            chords_simplified = remove_too_short_chords(chords_simplified, 0.15)
            chords_simplified = simplify_predicted_chords(chords_simplified)

            chords_simplified.to_csv('chords_simplified.csv')

            #Generate a .srt file from the predicted chords
            subtitles = create_subtitles(chords_simplified)

            #Merge subtitles into the original container file
            output_file_name = video_id + '_subtitled.mp4'
            result = burn_subtitles_to_video(video, output_file_name)

            f = open(output_file_name, 'rb')
            video = Video(video_id = video_id, title = title, artist = artist, song = song, chords = ugChords, result_video = File(f) )
            video.save()
            return Response(VideoSerializer(video).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UGChordView(generics.ListCreateAPIView):
    queryset = UGChords.objects.all()
    serializer_class = UGChordSerializer

class ChromaToChordView(generics.ListCreateAPIView):
    queryset = ChromaToChord.objects.order_by('-id')[:10]
    serializer_class = ChromaToChordSerializer

class AveragedChordsView(generics.ListCreateAPIView):
    queryset = AveragedChords.objects.all()
    serializer_class = AveragedChordsSerializer

def upload_chroma_to_chord(some):
    # ChromaToChord.objects.all().delete()

    nr = ChromaToChord.objects.count()
    logger.error("################# NR OF ROWS")
    logger.error(nr)

    # with open("training_data.csv") as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         _, created = ChromaToChord.objects.get_or_create(
    #             C = row[1],
    #             Cs = row[2],
    #             D = row[3],
    #             Ds = row[4],
    #             E = row[5],
    #             F = row[6],
    #             Fs = row[7],
    #             G = row[8],
    #             Gs = row[9],
    #             A = row[10],
    #             As = row[11],
    #             B = row[12],
    #             chord = row[15],
    #             cleaned_chord = row[16]
    #         )

def upload_averaged_chords(some):

    with open("training_data_grouped.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = AveragedChords.objects.get_or_create(
                cleaned_chord = row[0],
                C = row[1],
                Cs = row[2],
                D = row[3],
                Ds = row[4],
                E = row[5],
                F = row[6],
                Fs = row[7],
                G = row[8],
                Gs = row[9],
                A = row[10],
                As = row[11],
                B = row[12],
                count = row[13]
            )


def upload_chords(some):
    with open("unique_chords.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = UGChords.objects.get_or_create(
                artist=row[1],
                song=row[2],
                capo=row[3],
                ug_chords=row[4]
            )
