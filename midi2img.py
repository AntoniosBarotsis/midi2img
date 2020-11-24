from music21 import converter, instrument, note, chord
import json
import sys
import numpy as np
from imageio import imwrite

def extractNote(element):
    return int(element.pitch.ps)

def extractDuration(element):
    return element.duration.quarterLength

def get_notes(notes_to_parse):

    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    durations = []
    notes = []
    start = []

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            if element.isRest:
                continue

            start.append(element.offset)
            notes.append(extractNote(element))
            durations.append(extractDuration(element))
                
        elif isinstance(element, chord.Chord):
            if element.isRest:
                continue
            for chord_note in element.notes:
                start.append(element.offset)
                durations.append(extractDuration(element))
                notes.append(extractNote(chord_note))

    return {"start":start, "pitch":notes, "dur":durations}

def midi2image(midi_path, reps):
    try:
        mid = converter.parse(midi_path)
    except Exception:
        f = open("out.log", "a")
        f.write(f"FAILING PATH: {midi_path}")
        f.close()
        return
        
    instruments = instrument.partitionByInstrument(mid)

    data = {}

    try:
        i=0
        for instrument_i in instruments.parts:
            notes_to_parse = instrument_i.recurse()

            if instrument_i.partName is None:
                data["instrument_{}".format(i)] = get_notes(notes_to_parse)
                i+=1
            else:
                data[instrument_i.partName] = get_notes(notes_to_parse)
    except Exception:
        notes_to_parse = mid.flat.notes
        data["instrument_0".format(i)] = get_notes(notes_to_parse)

    resolution = 0.25

    for instrument_name, values in data.items():
        # https://en.wikipedia.org/wiki/Scientific_pitch_notation#Similar_systems
        upperBoundNote = 127
        lowerBoundNote = 21
        maxSongLength = 100

        index = 0
        prev_index = 0
        repetitions = 0
        while repetitions < int(reps):
            if prev_index >= len(values["pitch"]):
                break

            # Filter out songs that do not include piano here to save time
            if "piano" not in instrument_name.lower():
                index += 1
                repetitions+=1
                continue

            matrix = np.zeros((upperBoundNote-lowerBoundNote,maxSongLength))

            pitchs = values["pitch"]
            durs = values["dur"]
            starts = values["start"]

            for i in range(prev_index,len(pitchs)):
                pitch = pitchs[i]

                dur = int(durs[i]/resolution)
                start = int(starts[i]/resolution)

                if dur+start - index*maxSongLength < maxSongLength:
                    for j in range(start,start+dur):
                        if j - index*maxSongLength >= 0:
                            matrix[pitch-lowerBoundNote,j - index*maxSongLength] = 255
                else:
                    prev_index = i
                    break

            # Remove empty and nearly empty images
            if (np.all(matrix == 0) or is_almost_empty(matrix)):
                index += 1
                repetitions+=1
                continue

            try:
                imwrite("imgOut/" + midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}.png"),matrix)
            except Exception:
                f = open("out.log", "a")
                f.write(midi_path.split("/")[-1].replace(".mid",f"_{instrument_name}_{index}.png") + "\n")
                f.close()

            index += 1
            repetitions+=1

def main_midi(midi_path, reps):
    import sys
    midi2image(midi_path, reps)

def is_almost_empty(matrix):
    count = 0
    maxCount = 0
    for i in range(0, matrix[0].size):
        if np.all(matrix[:,i] == 0):
            count = count + 1
            
            if maxCount < count:
              maxCount = count
        else:
            count = 0

    return maxCount > 18;

# import sys
# midi_path = sys.argv[1]
# midi2image(midi_path)