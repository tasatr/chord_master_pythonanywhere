import datetime
import os
import ffmpeg

filePath = 'chord_subtitles.srt';

def create_subtitles(chords_simplified):
    if os.path.exists(filePath):
        os.remove(filePath)

    counter = 1
    with open(filePath, 'a') as the_file:

        for idx, ch in chords_simplified.iterrows():
            the_file.write(str(counter) + '\n')

            chord = ch['predicted']
            if ch['predicted'].startswith('<'):
                chord = ''

            seconds = ch['start']
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)

            start_time = "%02d:%02d:%02d"%(hours,minutes,seconds)
            number_dec = str(ch['start']-int(ch['start']))[2:4]
            start_time = start_time + ',' + number_dec

            seconds = ch['end']
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)

            end_time = "%02d:%02d:%02d"%(hours,minutes,seconds)
            number_dec = str(ch['end']-int(ch['end']))[2:4]
            end_time = end_time + ',' + number_dec

            the_file.write(start_time + ' --> ' + end_time + '\n')
            if (idx < len(chords_simplified)-1):
                chord_row = str(chord + '        Next: ' + chords_simplified.iloc[idx + 1]['predicted'] + '\n')
                the_file.write(chord_row)
            else:
                the_file.write(chord + '\n')
            the_file.write('\n')

            counter = counter + 1
    return filePath

def burn_subtitles_to_video(video_file_name, output_file_name):
    stream = ffmpeg.input(video_file_name)
    audio_stream = stream['a']
    video_stream = stream['v']

    video_stream = ffmpeg.filter(video_stream, 'subtitles', filePath)
    joined = ffmpeg.concat(video_stream, audio_stream, v=1, a=1)
    out_stream = ffmpeg.output(joined, output_file_name)
    ffmpeg.run(out_stream)
