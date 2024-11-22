import os
from textnode import *
from htmlnode import *
from helper import *

def main():
    # Try a test string
    result = text_to_textnodes("Here's an ![image](url) with **bold** and a [link](url) and some `code`")

    # Print the results
    for node in result:
        print(f"Text: {node.text}, Type: {node.text_type}, Url: {node.url}")

main()
