from textnode import TextNode
from textnode import TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.TextType != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)  
            for index, node in enumerate(split_nodes):
                if index % 2 == 0:
                    new_nodes.append(TextNode(node, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(node, text_type))
    return new_nodes
            
def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links



    

