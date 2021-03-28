import numpy as np

mapping = {'48': 'z', '50': 'x', '52': 'c', '53': 'v', '55': 'b', '57': 'n', '59': 'm', '60': 'a', '62': 's', '64': 'd', '65': 'f', '67': 'g', '69': 'h', '71': 'j', '72': 'q', '74': 'w', '76': 'e', '77': 'r', '79': 't', '81': 'y', '83': 'u'}
mapping_vector = np.zeros([128])
mapping_keys = list(mapping.keys())
for key in mapping_keys:
    mapping_vector[int(key)] = 1  # higher pitch should be assigned more weight?

def note_density(track):
    density_vector = np.zeros([128])
    # for note in track:
    #     print(note["note"])
    for note in track:
        density_vector[note["note"]] += 1
    return density_vector

def calculate_match(track, mapping_vec):
    track_note_density = note_density(track)
    match_ratio = np.dot(track_note_density, mapping_vec) / np.sum(track_note_density)
    return match_ratio

def get_shift_best_match(track, bounds=[-21,21]):
    best_shift = 0
    best_match = 0
    for shift in range(*bounds):
        shifted_keys = [int(k)+shift for k in mapping_keys]
        shifted_mapping = np.zeros([128])
        for key in shifted_keys:
            shifted_mapping[key] = 1  # higher pitch should be assigned more weight?
        match_score = calculate_match(track, shifted_mapping)
        if match_score > best_match:  # higher shift takes priority
            best_match = match_score
            best_shift = shift
    return -best_shift, best_match