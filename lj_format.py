import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def create_if_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

def generate_entry(output_path, wav_path, id, gnd_truth_lst):
    file_name = os.path.splitext(os.path.basename(wav_path))[0]
    gnd_truth_index = int(file_name.split('_')[-1]) - 1
    gnd_truth = gnd_truth_lst[gnd_truth_index]

    shutil.copy(wav_path, os.path.join(output_path, 'wav', f'LJ{str(id).zfill(4)}.wav'))
    return {"ID" : f'LJ{str(id).zfill(4)}', "text" :  gnd_truth, "text cleaned" : gnd_truth} 

def get_artic_gnd_truth(path):
    arr = []
    with open(path, 'r') as f:
        arr = [line.rstrip() for line in f]
    return [l[findnth(l, ' ', 1) + 2:-3] for l in arr]

gnd_truth_path = '/home/nam/scifilab/Audio-to-Voice-Dataset/cmuarctic.data.txt'
wav_folder = '/home/nam/scifilab/Audio-to-Voice-Dataset/jenie_Disgusted_16bits'
output_path = '/home/nam/scifilab/Audio-to-Voice-Dataset/output2'

gnd_truth_lst = get_artic_gnd_truth(gnd_truth_path)


wav_files = [os.path.join(wav_folder, i) for i in sorted(os.listdir(wav_folder))]

output_path_duplicate = [output_path for i in range(len(wav_files))]
gnd_truth_lst_duplicate = [gnd_truth_lst for i in range(len(wav_files))]

ids = [i for i in range(1, len(wav_files) + 1)]

create_if_not_exist(os.path.join(output_path, 'wav'))

with ThreadPoolExecutor(max_workers=20) as executor:
    metadata = list(executor.map(generate_entry, output_path_duplicate, wav_files, ids, gnd_truth_lst_duplicate))

metadata_df = pd.DataFrame(metadata)
metadata_path = os.path.join(os.path.join(output_path, 'metadata.csv'))
metadata_df.to_csv(metadata_path, sep = '|', header=False, index=False)

