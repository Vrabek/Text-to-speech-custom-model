

class InitJsonData:

    def __init__(self, json_data: dict):

        if not isinstance(json_data, dict):
            raise ValueError('Invalid JSON data type. Expected dict, got {}'.format(type(json_data)))
        elif self.has_sufficient_structure(json_data) is False:
            raise ValueError('Invalid JSON file structure. Required keys: id, filename, extension, transcript')
        
        self.json_data = json_data

    def __str__(self):
        return 'InitJsonData: {}'.format(self.json_data)
    
    def has_sufficient_structure(self, json_data: dict = None):

        if json_data is None:
            json_data = self.json_data

        required_keys = ['id', 'filename', 'extension', 'transcript']

        if not all(key in json_data for key in required_keys):
            raise ValueError('Invalid JSON file structure. Required keys: id, filename, extension, transcript')
        
        return True
    
    def get_full_filename(self):
        return self.json_data['filename'] + '.' + self.json_data['extension']
    
    def get_transcript(self):
        return self.json_data['transcript']
    
    def get_id(self):
        return self.json_data['id']
    
    def prepare_json_data(self):

        if self.has_sufficient_structure():

            full_filename = self.get_full_filename()
            transcript = self.get_transcript()
            id = self.get_id()

            #print(filename, full_filename, transcript, id)
            foramted_json = {
                'id': id,
                'filename': full_filename,
                'transcript': transcript
                
            }
            return foramted_json



        return self.json_data

    

class AudioFile:

    def __init__(self, json_data: InitJsonData):

        if not isinstance(json_data, InitJsonData):
            raise ValueError('Invalid JSON data type. Expected InitJsonData, got {}'.format(type(json_data)))
        elif json_data.has_sufficient_structure() is False:
            raise ValueError('Invalid JSON file structure. Required keys: id, transcript_filename, audio_filename')

        self.json_data = json_data
    
    def get_audio_filename(self):
        return self.json_data.get_full_filename()


class AlignedJson(InitJsonData):

    def __init__(self, json_data: dict):

        self.json_data = json_data
    
    def has_sufficient_structure(self):
        
        required_keys = ['id', 'transcript_filename', 'audio_filename']

        if not all(key in self.json_data for key in required_keys):
            raise ValueError('Invalid JSON file structure. Required keys: id, transcript_filename, audio_filename')
        
        return True
    

class Runtime:

    def __init__(self, json_list: list, audio_file: AudioFile=None):

        self.json_list = json_list
        self.audio_file = audio_file

        self.temp_data = []
    
    def process_data(self):

        for json_data in self.json_list:

            print(json_data)

            init_json = InitJsonData(json_data)
            print(init_json)

            if init_json.has_sufficient_structure():
                formated_json = InitJsonData(json_data).prepare_json_data()
                self.temp_data.append(formated_json)
                print(formated_json)


        