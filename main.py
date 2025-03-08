from classes import *
import json

if __name__ == "__main__":

    path_to_mp3_files = 'jc-voicelines'
    
    #LOAD JSON FILE into a dictionary
    with open('results.json') as f:
        data = json.load(f)

    run = Runtime(data)
    run.process_data()
    run.convert_mp3_to_wav(path_to_mp3_files)