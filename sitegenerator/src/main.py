import functions

def main():
    functions.copy_contents("static", "public")
    functions.generate_pages_recursive("content", "template.html", "public")


main()