from textnode import *
from htmlnode import *
from enums import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            for alt, url in images:
                before, after = node.text.split(f"![{alt}]({url})",1)
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE,url))
                node.text = after
            if node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            for alt, link in links:
                before, after = node.text.split(f"[{alt}]({link})",1)
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK,link))
                node.text = after
            if node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n\n"):
        cleaned_line = line.strip()
        if cleaned_line:
            blocks.append(cleaned_line)
    return blocks

def block_to_block_type(block):
        if re.match(r"#+", block):
        # TODO: Add  additional types for H1, H2, H3, etc. and add another shitty loop to tag em all out
            return BlockType.HEADING
        elif block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
        elif re.match(r"> ", block):
            # More shitty loops
            return BlockType.QUOTE
        elif block.startswith("- ") or block.startswith("* "):
            # Write a really annoying for loop splitting the block and checking if each line starts with a bullet point
            return BlockType.UNORDERED_LIST
        elif block.startswith("1. "): 
            # Write another shitty for loop to check that the numbers increment by one
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH


