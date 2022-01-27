from os import path, listdir
import json
from urllib.parse import urljoin, urlparse

# Temporary Global var cache directory
cache_directory = path.abspath("./site_cache")

# url = "https://www.sciencealert.uk"
# # Domain name of the URL


# file_path = path.abspath("./site_cache/test.json")
# print("==========================")

# urls = set(())

# with open(file_path, "r") as read_file:
#     data = json.load(read_file)
#     for url in data["urls"]:
#         urls.add(url)

# site_map_json = {
#     "urls": list(urls)
# }

# write_file = domain_name = urlparse(url).netloc
# write_path = "./site_cache/" + write_file +".json"
# write_path = path.abspath(write_path)

# with open(write_path, "w") as write_file:
#     json.dump(site_map_json, write_file)

def cache_file_name_from_url(url):
    try:
        return urlparse(url).netloc + ".json"
    except:
        return None
        
# Returns all the file names in cache
def get_file_names():
    try:
        file_names = listdir(cache_directory)
        return file_names
    except FileNotFoundError:
        return []

# Returns true if file in cache
def file_exists(file_name):
    files_in_cache = set(get_file_names())
    if file_name in files_in_cache:
        return True
    else:
        return False

def file_has_key(file_name, key):
    try:
        cache_file_content = get_file_contents(file_name)
        if key in cache_file_content:
            print("True")
            return True
        else:
            print("False")
            return False
    except FileNotFoundError:
        return False

# Returns file contents
def get_file_contents(file_name):
    try:
        file_path = path.abspath(cache_directory + "/" + file_name)
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        return data
    except FileNotFoundError:
        return []
