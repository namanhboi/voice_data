import soundfile
import os
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys

def convert_16bits(args):
    wav_path, output_path = args
    data, samplerate = soundfile.read(wav_path)
    soundfile.write(os.path.join(output_path, os.path.basename(wav_path)), data = data ,samplerate=samplerate, subtype='PCM_16')
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-wp', '--wav-path', help = 'path to folder containing the wav files')
    parser.add_argument('-op', '--output-path', help = 'folder to output the converted wav files')
    args = parser.parse_args()
    if not os.path.exists(args.wav_path):
        print("wav path does not exist")
        sys.exit(1)
    if not os.path.exists(args.output_path):
        print("output path doesn't exist")
        sys.exit(1)
    
    wav_paths = [os.path.join(args.wav_path, path) for path in sorted(os.listdir(args.wav_path))]
    arguments = [(i, args.output_path) for i in wav_paths]
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(convert_16bits, arguments))

    print('done')