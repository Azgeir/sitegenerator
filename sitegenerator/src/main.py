import functions


def main():
    functions.copy_contents("static", "public")
    functions.generate_page("content/index.md", "template.html", "public/index.html")




main()