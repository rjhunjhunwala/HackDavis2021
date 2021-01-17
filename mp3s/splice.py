from pydub import AudioSegment

sound = AudioSegment.from_mp3("chromatic.mp3")

# len() and slicing are in milliseconds
millis_per_note = len(sound) / 88
second_half = sound[halfway_point:]

for i in range(88):
    note = sound[i * millis_per_note: i * millis_per_note + millis_per_note]
    note = note[130:-130]
    note.export(str(i) + ".mp3", format="mp3")