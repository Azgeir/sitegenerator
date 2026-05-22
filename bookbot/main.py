import sys
from stats import count_words, count_characters, sort_dictionary

def get_book_text(filepath):
    with open(filepath) as f:
        return f.read()



def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {sys.argv[1]}...")
    print("----------- Word Count ----------")
    print(f"Found {count_words(get_book_text(sys.argv[1]))} total words")
    print("--------- Character Count -------")
    for character in sort_dictionary(count_characters(get_book_text(sys.argv[1]))):
        if character["char"].isalpha():
            print(f"{character["char"]}: {character["num"]}")
    print("============= END ===============")
    



main()
