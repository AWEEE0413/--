from pydub import AudioSegment
from datetime import datetime

def mix_audio(song_path, recording):
    # Load the song
    song = AudioSegment.from_file(song_path)

    # Convert the recording to an AudioSegment
    recording_segment = AudioSegment(
        recording.tobytes(), 
        frame_rate=44100,
        sample_width=recording.dtype.itemsize, 
        channels=2
    )

    # Mix the song and the recording
    mixed = song.overlay(recording_segment)

    # Save the mixed audio
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    mixed.export("mixed_audio.mp3", format="mp3")