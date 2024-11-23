from textnode import *
from splitter import *
from markdown import *
from enums import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
        
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag Missing")
        if self.children is None:
            raise ValueError("Children is Missing and Mandatory")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt":
                            text_node.text})
        case _:
            raise ValueError("Invalid Text Type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = []
    for block in blocks:
       block_type = block_to_block_type(block) 
       match block_type:
        case BlockType.HEADING1:
                html.append(HTMLNode(tag=HTMLType.HEADING1, children=text_to_children(block)))
        case BlockType.HEADING2:
                html.append(HTMLNode(tag=HTMLType.HEADING2, children=text_to_children(block)))
        case BlockType.HEADING3:
                html.append(HTMLNode(tag=HTMLType.HEADING3, children=text_to_children(block)))
        case BlockType.HEADING4:
                html.append(HTMLNode(tag=HTMLType.HEADING4, children=text_to_children(block)))
        case BlockType.HEADING5:
                html.append(HTMLNode(tag=HTMLType.HEADING5, children=text_to_children(block)))
        case BlockType.HEADING6:
                html.append(HTMLNode(tag=HTMLType.HEADING6, children=text_to_children(block)))
        case BlockType.CODE:
                pre_node = HTMLNode(tag=HTMLType.CODEPRE)
                pre_node.children = [HTMLNode(tag=HTMLType.CODE, text=block)]
                html.append(pre_node)
        case BlockType.QUOTE:
                html.append(HTMLNode(tag=HTMLType.QUOTE, children=text_to_children(block)))
        case BlockType.UNORDERED_LIST:
                pre_node = HTMLNode(tag=HTMLType.UNORDERED_LIST)
                pre_node.children = text_to_list_children(block)
                html.append(pre_node)
        case BlockType.ORDERED_LIST:
                pre_node = HTMLNode(tag=HTMLType.ORDERED_LIST)
                pre_node.children = text_to_list_children(block)
                html.append(pre_node)
        case BlockType.PARAGRAPH:
                html.append(HTMLNode(tag=HTMLType.PARAGRAPH, children=text_to_children(block)))
    return HTMLNode(tag=HTMLType.DIV, children=html)

def text_to_children(text):
    children = []
    text_nodes = text_to_text_nodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def text_to_list_children(text):
    list_items = text.split("\n")
    list_item_nodes = []
    for item in list_items:
        cleaned_item = re.sub(r"^[\-\*\+]\s+", "", item)
        text_nodes = text_to_text_nodes(cleaned_item)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        li_node = HTMLNode(tag=HTMLType.LIST_ITEM, children=html_nodes)
        list_item_nodes.append(li_node)
    return list_item_nodes



