from os import path
import json

file_path = path.abspath("./site_cache/test.json")
print("==========================")

with open(file_path, "r") as read_file:
    data = json.load(read_file)
    print(data)