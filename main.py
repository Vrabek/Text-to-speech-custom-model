from classes import *
import json

if __name__ == "__main__":
    
    #LOAD JSON FILE into a dictionary
    with open('results.json') as f:
        data = json.load(f)

    run = Runtime(data)
    run.process_data()