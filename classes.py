import os
import re
import torchaudio
from torch.utils.data import Dataset
from pydub import AudioSegment

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

            formatted_json = {
                'id': id,
                'filename': full_filename,
                'transcript': transcript               
            }
            return formatted_json

        return self.json_data

    
class MP3toWAVConverter:
    def __init__(self, filename: str, source_file_location: str):
        self.location = source_file_location
        self.filename = filename
    
    def file_exists(self):
        path = os.path.join(self.location, self.filename)
        if os.path.exists(path):
            return True
    
    def file_is_mp3(self):
        if self.filename.endswith('.mp3'):
            return True
        
    def get_full_path(self):
        return os.path.join(self.location, self.filename)
    
    def create_wav_folder(self):
        wav_folder_path = os.path.join('wav_files')
        if not os.path.exists(wav_folder_path):
            os.makedirs(wav_folder_path)
        return wav_folder_path
    
    def convert_to_wav(self):
        
        wav_folder_path = self.create_wav_folder()

        #self.filename_cleanup(self.location)

        if self.file_exists() and self.file_is_mp3():
            mp3_path = self.get_full_path()
            wav_file = self.filename.replace('.mp3', '.wav') 
            wav_path = os.path.join(wav_folder_path, wav_file)

            self.create_wav_folder()

            if not os.path.exists(wav_path):
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")

                print("Conversion complete! WAV file saved as", wav_path)
        else:
            raise ValueError(f'{self.location}\{self.filename} File does not exist or is not an MP3 file')
        
    
    @staticmethod
    def filename_cleanup(path: str):
        
        for filename in os.listdir(path):
            
            name, ext = os.path.splitext(filename)

            # If the name ends with multiple dots, clean them
            cleaned_name = re.sub(r'\.+$', '', name)
            # Reconstruct the filename
            fixed_filename = f"{cleaned_name}.{ext.lstrip('.')}" if ext else cleaned_name
            # Return the original filename if no changes were made
            # return fixed_filename 
            if fixed_filename != filename:
                print(f'Renaming: {filename} to {fixed_filename}')
                os.rename(os.path.join(path, filename), os.path.join(path, fixed_filename))

class Runtime:

    def __init__(self, json_list: list):

        self.json_list = json_list
        self.temp_data = []
    
    def process_data(self):

        for json_data in self.json_list:

            init_json = InitJsonData(json_data)

            if init_json.has_sufficient_structure():
                formated_json = InitJsonData(json_data).prepare_json_data()
                self.temp_data.append(formated_json)
                
        print(self.temp_data)


    def convert_mp3_to_wav(self, location: str):
        for json_data in self.temp_data:
            filename = json_data['filename']
            converter = MP3toWAVConverter(filename, location)
            print('json_data:', json_data)
            #clean the source data
            converter.filename_cleanup(location)
            #perform the conversion
            converter.convert_to_wav()