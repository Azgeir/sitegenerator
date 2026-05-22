import functions
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    functions.copy_contents("static", "docs")
    functions.generate_pages_recursive("content", "template.html", "docs", basepath)
    print(f"sys.argv = {sys.argv}")
    print(f"basepath = {basepath}")


main()