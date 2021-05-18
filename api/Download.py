import youtube_dl
import os
from spleeter.separator import Separator
import glob

class Download:
    @staticmethod
    def separate_vocal():
        # Using embedded configuration.
        separator = Separator('spleeter:2stems')
        from spleeter.audio.adapter import AudioAdapter

        separator.separate_to_file('temp.mp3', 'audio_output')
        return

    @staticmethod
    def download_mp3(video_id):
        #delete existing temp.mp3 file
        file_path = 'temp.mp3'
        if os.path.exists(file_path):
            os.remove(file_path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + video_id])

    @staticmethod
    def download_video(video_id):
        #delete existing temp.mp3 file
        file_path = 'temp.mp4'
        if os.path.exists(file_path):
            os.remove(file_path)

        ydl_opts = {
            'outtmpl': 'temp_video'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            filename = ydl.download(['http://www.youtube.com/watch?v=' + video_id])

            filenames = glob.glob('temp_video.*')
            if os.path.exists(filenames[0]):
                return filenames[0]

            return 'missingvideo.mp4'
