

class JsonHandler:

    def __init__(self, json_data: dict):

        if not isinstance(json_data, dict):
            raise ValueError('Invalid JSON data type. Expected dict, got {}'.format(type(json_data)))
        elif self.has_sufficient_structure(json_data) is False:
            raise ValueError('Invalid JSON file structure. Required keys: id, filename, extension, transcript')
        
        self.json_data = json_data


    
    def has_sufficient_structure(self):

        required_keys = ['id', 'filename', 'extension', 'transcript']

        if not all(key in self.json_data for key in required_keys):
            raise ValueError('Invalid JSON file structure. Required keys: id, filename, extension, transcript')
        
        return True
    
    def get_full_filename(self):
        return self.json_data['filename'] + '.' + self.json_data['extension']
    
    def get_transcript(self):
        return self.json_data['transcript']