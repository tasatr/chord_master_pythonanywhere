from django.urls import path
from .views import VideoView, CreateVideoView, UGChordView, ChromaToChordView, AveragedChordsView
from .views import upload_chords, upload_chroma_to_chord, upload_averaged_chords

urlpatterns = [
    path('', VideoView.as_view()),
    path("create-video", CreateVideoView.as_view()),
    path("list-videos", VideoView.as_view()),
    path("upload-chords", upload_chords, name="upload_chords"),
    path("list-ug-chords", UGChordView.as_view()),
    path("upload-chroma-to-chord", upload_chroma_to_chord, name="upload_chroma_to_chord"),
    path("upload-averaged-chords", upload_averaged_chords, name="upload_averaged_chords"),
    path("list-chroma-to-chord",ChromaToChordView.as_view() ),
    path("list-averaged-chords", AveragedChordsView.as_view() )
]
