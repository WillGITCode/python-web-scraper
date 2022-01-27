# Remove duplicates from list
def remove_list_duplicates(list):
    seen = set()
    seen.update(list)
    return list(seen)