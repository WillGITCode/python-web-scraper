from os import path, listdir
import json
import os
from urllib.parse import urljoin, urlparse
from utilities import file_util

class CacheService:
    def __init__(self):
        # Temporary Global cache directory
        self.cache_directory = path.abspath("./site_cache")
        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)

    def get_cache_name_from_url(self, url):
        try:
            return urlparse(url).netloc.split(".")[-2] + ".json"
        except:
            return None

    # Returns true if file in cache
    def site_cache_exists(self, cache_name):
        files_in_cache = set(file_util.get_directory_file_names(self.cache_directory))
        if files_in_cache is not None and cache_name in files_in_cache:
            return True
        else:
            return False

    def cache_has_key(self, cache_name, key):
        try:
            file_path = path.abspath(self.cache_directory + "/" + cache_name)
            cache_file_content = file_util.get_file_contents(file_path)
            if key in cache_file_content:
                return True
            else:
                return False
        except:
            return False

    # Sets file contents
    def new_site_cache(self, cache_name, content):
        try:
            file_path = path.abspath(self.cache_directory + "/" + cache_name)
            file_util.set_file_contents(file_path, content)
        except:
            print("Error: Could not set site cache", cache_name)
    
    # Sets file contents
    def set_site_cache(self, url, content):
        try:
            cache_name = self.get_cache_name_from_url(url)
            file_path = path.abspath(self.cache_directory + "/" + cache_name)
            site_cache = {
                "urls": content
            }
            file_util.set_file_contents(file_path, site_cache)
        except:
            print("Error: Could not set site cache", cache_name)

    # Sets file contents
    def get_site_cache(self, url):
        try:
            cache_name = self.get_cache_name_from_url(url)
            file_path = path.abspath(self.cache_directory + "/" + cache_name)
            site_cache = file_util.get_file_contents(file_path)
            return site_cache
        except:
            print("Error: Could not get site cache", cache_name)
            return None
