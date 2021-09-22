from .flashcard import AudioPlayer

# Initialize the audio player singleton. This is because VLC instance can't be created from GUI
AudioPlayer.instance()
