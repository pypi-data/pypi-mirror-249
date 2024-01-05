import os
import tempfile
import moviepy.editor

from pathlib import Path


def convert(input, output=None):
    if output is None:
        output = os.getcwd()
    try:
        video_path = open(input, 'rb')  # open video media as binary
    except OSError:
        print(OSError.strerror)

    tf = tempfile.NamedTemporaryFile()  # create a temporary file
    tf.write(video_path.read())  # store the binary file in temp file
    print("Conversion in progress... 🎉")
    audio = moviepy.editor.VideoFileClip(tf.name).audio  # extra audio media
    tf.close()  # close the temp file to free memory

    audio_file = input.split('.')  # remove all '.' in video file name
    audio_file.pop()  # move the last element(mp4 or avi etc...) in my list
    audio_file.append('mp3')  # add mp3 like last element in my list
    audio_file = ".".join(elt for elt in audio_file)  # build the audio name
    audio_path = Path("%s/%s" % (output, audio_file))  # buid audio path

    audio.write_audiofile(audio_path)  # write audio media to audio_path
    print("Audio file was created successfuly ! 🔊")


if __name__ == '__main__':
    convert()


# e.g: python script_name.py --input=path/to/video/file.mp4
# .      --output=path/to/audio/file.mp3
