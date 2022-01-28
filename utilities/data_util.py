# Remove duplicates from list
def remove_list_duplicates(list_to_clean):
    seen = set(())
    seen.update(list_to_clean)
    return list(seen)