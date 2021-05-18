from django.db import models

# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000, default='artist')
    song = models.CharField(max_length=1000, default='song')
    chords = models.TextField()
    result_video = models.FileField(upload_to="video/%y")
    created_date = models.DateTimeField(auto_now_add=True)

    def set_chords(self, chordSequence):
        self.chords = chordSequence
        self.save()

    def __str__(self):
        return self.title

class UGChords(models.Model):
    artist = models.CharField(max_length=1000)
    song = models.CharField(max_length=1000)
    ug_chords = models.TextField()
    capo = models.SmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

class ChromaToChord(models.Model):
    C = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Cs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    D = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Ds = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    E = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    F = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Fs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    G = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Gs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    A = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    As = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    B = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    chord = models.TextField()
    cleaned_chord = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class AveragedChords(models.Model):
    C = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Cs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    D = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Ds = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    E = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    F = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Fs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    G = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    Gs = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    A = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    As = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    B = models.DecimalField(decimal_places=9, max_digits=10,default=0)
    cleaned_chord = models.TextField()
    count = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
