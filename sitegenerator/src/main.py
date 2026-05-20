from textnode import TextNode, TextType
import shutil
import os


def main():
    textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textnode)

def copy_contents(src, dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    copy(src, dir)

def copy(src, dir):
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        target_path = os.path.join(dir, file)
        if not os.path.isfile(file_path):
            os.mkdir(target_path)
            copy(file_path, target_path)
        else:
            shutil.copy(file_path, target_path)


main()