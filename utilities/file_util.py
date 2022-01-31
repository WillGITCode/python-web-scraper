from os import path, listdir
import json

def get_directory_file_names(directory):
    try:
        file_names = listdir(directory)
        return file_names
    except FileNotFoundError as error:
        return error

# Returns file contents
def get_file_contents(file_path):
    try:
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        return data
    except FileNotFoundError:
        return None

def set_file_contents(file_path, content):
    try:
        with open(file_path, "w") as write_file:
            json.dump(content, write_file)
    except:
        print("Error: Could not set file contents", file_path)