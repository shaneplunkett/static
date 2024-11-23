import os
import shutil

def copy_html():
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)
    if os.path.exists("../public"):
        print(f"Deleting Old Files")
        shutil.rmtree("../public")
    print(f"Making New Public Directory")
    print(f"Copying Files from Static to Public")
    shutil.copytree("../static", "../public")

def generate_page(from_path, template_path, dest_path):
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)
    print(f"Generating Page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    return None
