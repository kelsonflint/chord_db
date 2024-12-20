import json

# Guitar strings based on standard tuning
guitar_strings = {
    "6": 20,  # E2
    "5": 25,  # A2
    "4": 30,  # D3
    "3": 35,  # G3
    "2": 39,  # B3
    "1": 44   # E4
}

guitar_length = 13

# Generate all 88 piano notes
def generate_notes():
    note_names = [
        "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"
    ]
    notes = {}
    hz = 27.5  # Starting frequency for A0
    for i in range(88):
        octave = (i // 12) + 1  # Determine octave
        note_name = f"{note_names[i % 12]}{octave}"
        notes[i + 1] = {
            "noteId": i + 1,
            "pitch": note_names[i % 12],
            "octave": octave,
            "name": note_name,
            "Hz": round(hz, 3)
        }
        hz *= 2 ** (1 / 12)  # Increment frequency by a semitone
    return notes

# Full 88-note dictionary
notes = generate_notes()

# Chord intervals map (in semitones)
chords_map = {
    "Major": [0, 4, 7],          # U, M3, P5
    "Minor": [0, 3, 7],          # U, m3, P5
    "Diminished": [0, 3, 6],     # U, m3, d5
    "Augmented": [0, 4, 8],      # U, M3, A5
    "Major 7th": [0, 4, 7, 11],  # U, M3, P5, M7
    "Minor 7th": [0, 3, 7, 10],  # U, m3, P5, m7
    "Dominant 7th": [0, 4, 7, 10], # U, M3, P5, m7
    "Sus2": [0, 2, 7],           # U, M2, P5
    "Sus4": [0, 5, 7],           # U, P4, P5
    "Diminished 7th": [0, 3, 6, 9],  # U, m3, d5, d7
    "Major 9th": [0, 4, 7, 11, 14], # U, M3, P5, M7, M9
    "Minor 9th": [0, 3, 7, 10, 13], # U, m3, P5, m7, m9
    "Dominant 9th": [0, 4, 7, 10, 14], # U, M3, P5, m7, M9
}

# Chord intervals map (in semitones)
chords_notation_map = {
    "Major": "",          # U, M3, P5
    "Minor": "m",          # U, m3, P5
    "Diminished": "dim",     # U, m3, d5
    "Augmented": "aug",      # U, M3, A5
    "Major 7th": "maj7",  # U, M3, P5, M7
    "Minor 7th": "min7",  # U, m3, P5, m7
    "Dominant 7th": "7", # U, M3, P5, m7
    "Sus2": "sus2",           # U, M2, P5
    "Sus4": "sus4",           # U, P4, P5
    "Diminished 7th": "dim7",  # U, m3, d5, d7
    "Major 9th": "maj9", # U, M3, P5, M7, M9
    "Minor 9th": "min9", # U, m3, P5, m7, m9
    "Dominant 9th": "9", # U, M3, P5, m7, M9
}

# Function to build a chord
def build_chord(root_note_id, chord_name, notes):
    if chord_name not in chords_map:
        raise ValueError(f"Chord '{chord_name}' not found in chords_map")
    
    intervals = chords_map[chord_name]
    total_notes = len(notes)
    
    # Calculate the noteIds for the chord
    chord_note_ids = [(root_note_id - 1 + interval) % total_notes + 1 for interval in intervals]
    
    #return [notes[note_id] for note_id in chord_note_ids]
    return [notes[id]["pitch"] for id in chord_note_ids]

def select_strings(root_note_id, chord_notes):
    result = {}

    for string, open_note_id in sorted(guitar_strings.items(), reverse=True):
        
        for fret in range(0, guitar_length):
            note_id = open_note_id + fret
            note = notes[note_id]
            previousFret = result.get(string)
            if (note["pitch"] in chord_notes):
                if (string != 6 or result[string+1] == -1 and (fret - 3 <= previousFret and previousFret <= fret + 3)):
                    result.update({string: fret})
                    break
        else:
            result[string] = -1

    return result


# Generate chord database for root C3 (noteId = 28)
def generate_chord_database(root_note_id):
    chord_database = {}
    for chord_name in chords_map.keys():
        chord_notes = build_chord(root_note_id, chord_name, notes)
        #positions = map_chord_to_guitar_from_root(root_note_id, chord_name, notes)
        root = notes[root_note_id]
        chord_database[root["pitch"] + chords_notation_map[chord_name]] = {
            "id": root["pitch"] + chords_notation_map[chord_name],
            "displayName": root["name"][:-1] + " " + chord_name,
            "type": chord_name,
            "notes": chord_notes,
           # "strings": select_strings(root_note_id=root_note_id, chord_notes=chord_notes)
        }
    return chord_database

# Generate and save the database
root_note_id = 20  # C3
chord_database = {"chords": {}}
for i in range(root_note_id, 32):
    chord_database["chords"].update(generate_chord_database(i))

print(len(chord_database["chords"]))

# Save to JSON
output_file = "chord_note_db.json"
with open(output_file, "w") as file:
    json.dump(chord_database, file, indent=4)

print(f"Chord database generated and saved to {output_file}.")

