def count_words(book):
    return len(book.split())

def count_characters(book):
    character_count = {}
    for i in list(book):
        i = i.lower()
        if i not in character_count:
            character_count[i] = 1
        else:
            character_count[i] += 1
    return character_count

def sort_on(items):
    return items["num"]

def sort_dictionary(dictionary):
    sorted_dictionary = []
    for character in dictionary:
        sorted_dictionary += [
            {"char": character, "num": dictionary[character]}
        ]
    sorted_dictionary.sort(reverse=True, key=sort_on)
    return sorted_dictionary

