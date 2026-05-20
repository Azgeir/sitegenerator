from textnode import TextNode, TextType
import shutil
import os


def main():
    copy_contents("static", "public")

def copy_contents(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy(src, dest)

def copy(src, dest):
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        target_path = os.path.join(dest, file)
        print(f"Copying {file_path} to {target_path}")
        if not os.path.isfile(file_path):
            os.mkdir(target_path)
            copy(file_path, target_path)
        else:
            shutil.copy(file_path, target_path)


main()