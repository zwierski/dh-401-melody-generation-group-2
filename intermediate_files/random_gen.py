import random
import music21
import pandas as pd

random.seed(1113)

# fun to fill a bar with random notes
def random_bar():
    # first = True
    first = False
    # first decide how many notes are in the bar
    # (the tempo is always 3/4)
    bar = []
    for i in range(11):
        # decide if a note is played
        if first:
            bar.append(1.0)
            first = False
        elif random.random() < 0.5:
            # if yes, decide which note
            bar.append((i/4)+1)
        # check that the bar is not empty
    if len(bar) == 0:
        bar = random_bar()
    return bar

# create random song


def create_random_song():
    # make a list with 8 lists inside
    random_song = [[] for j in range(8)]
    # for each list in random_song fill it with random notes
    for i in range(8):
        random_song[i] = random_bar()
    return random_song


# example
random_song = create_random_song()
print('random song: ')
print(random_song)

# convert into duration


def convert_to_duration(random_song_list):
    last = 4.0
    # read the list backwards
    random_song_list.reverse()
    # create a list with the duration of each note
    duration_list = []
    for bar in random_song_list:
        # reverse the inner list
        bar.reverse()
        for note in bar:
            duration_list.append(last - note)
            last = note
        last += 4.0
    # reverse the list again
    duration_list.reverse()
    # return original order to original song aswell
    random_song_list.reverse()
    for bar in random_song_list:
        bar.reverse()
    return duration_list


# example
duration_list = convert_to_duration(random_song)
print('duration list: ')
print(duration_list)

# convert duration list into music21 stream


def convert_to_stream(duration_list):
    # create an empty stream
    stream = music21.stream.Stream()
    # define the tempo as 3/4
    stream.append(music21.meter.TimeSignature('3/4'))
    # create note
    # assign random pitch (C4)
    # assign duration (quarter)
    # append the note into empty stream
    for duration in duration_list:
        note = music21.note.Note(pitch='C4', quarterLength=duration)
        stream.append(note)
    return stream

# Function that maps the beat distribution of a bar to a series of numbers between 1 and 12 (position of each sixteenth-note in the bar)
def map_beats(notes):
    notes_mapped = []
    for bar in notes:
        bar_mapped = []
        for x in bar:
            bar_mapped.append(int(4*(x-1)+1))
        notes_mapped.append(bar_mapped)
    return notes_mapped


# example
stream = convert_to_stream(duration_list)
# print(type(stream))
# stream.show()

# play the stream
stream.show('midi')

# print with map_beats convertion
print('random song with map_beats: ')
print(map_beats(random_song))

# produce a dataframe size 500 samples and save it as csv
def produce_dataframe():
    df = pd.DataFrame()
    for i in range(500):
        random_song = create_random_song()
        df = df.append({'id': i, 'notes': map_beats(random_song)}, ignore_index=True)
    df.to_csv('random_songs.csv', index=False)
    return df

# example
df = produce_dataframe()
