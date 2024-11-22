import os
import shutil
from textnode import *
from htmlnode import *
from helper import *

def copy_html():
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)
    if os.path.exists("../public"):
        print(f"Deleting Old Files")
        shutil.rmtree("../public")
    print(f"Making New Public Directory")
    print(f"Copying Files from Static to Public")
    shutil.copytree("../static", "../public")

def main():

    copy_html()


if __name__ == "__main__":
    main()
