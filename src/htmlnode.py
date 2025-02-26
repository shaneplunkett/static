import re

from enums import BlockType, HTMLType, TextType
from markdown import block_to_block_type, markdown_to_blocks
from splitter import text_to_textnodes


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("No to_html method on HTMLNode")

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
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


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
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("Invalid Text Type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING1:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING1.value, children=header_to_children(block)
                    )
                )
            case BlockType.HEADING2:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING2.value, children=header_to_children(block)
                    )
                )
            case BlockType.HEADING3:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING3.value, children=header_to_children(block)
                    )
                )
            case BlockType.HEADING4:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING4.value, children=header_to_children(block)
                    )
                )
            case BlockType.HEADING5:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING5.value, children=header_to_children(block)
                    )
                )
            case BlockType.HEADING6:
                html.append(
                    ParentNode(
                        tag=HTMLType.HEADING6.value, children=header_to_children(block)
                    )
                )
            case BlockType.CODE:
                html.append(
                    ParentNode(
                        tag=HTMLType.CODEPRE.value, children=code_to_children(block)
                    )
                )
            case BlockType.QUOTE:
                html.append(
                    ParentNode(
                        tag=HTMLType.QUOTE.value, children=quote_to_children(block)
                    )
                )
            case BlockType.UNORDERED_LIST:
                html.append(
                    ParentNode(
                        tag=HTMLType.UNORDERED_LIST.value,
                        children=text_to_list_children(block),
                    )
                )
            case BlockType.ORDERED_LIST:
                html.append(
                    ParentNode(
                        tag=HTMLType.ORDERED_LIST.value,
                        children=text_to_list_children_ordered(block),
                    )
                )
            case BlockType.PARAGRAPH:
                html.append(
                    ParentNode(
                        tag=HTMLType.PARAGRAPH.value, children=text_to_children(block)
                    )
                )
    return ParentNode(tag=HTMLType.DIV.value, children=html)


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def header_to_children(text):
    cleaned_text = re.sub(r"^#+\s*", "", text)
    return text_to_children(cleaned_text)


def quote_to_children(text):
    cleaned_text = re.sub(r"^>\s*", "", text)
    return text_to_children(cleaned_text)


def code_to_children(text):
    cleaned_text = text[3:]
    children = text_to_children(cleaned_text)
    code = ParentNode(tag=HTMLType.CODE.value, children=children)
    return [code]


def text_to_list_children(text):
    list_items = text.split("\n")
    list_item_nodes = []
    for item in list_items:
        cleaned_item = re.sub(r"^\s*[\-\*\+]\s*", "", item).strip()
        text_nodes = text_to_textnodes(cleaned_item)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        li_node = ParentNode(tag=HTMLType.LIST_ITEM.value, children=html_nodes)
        list_item_nodes.append(li_node)
    return list_item_nodes


def text_to_list_children_ordered(text):
    list_items = text.split("\n")
    list_item_nodes = []
    for item in list_items:
        cleaned_item = re.sub(r"\d+\.\s*", "", item).strip()
        text_nodes = text_to_textnodes(cleaned_item)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        li_node = ParentNode(tag=HTMLType.LIST_ITEM.value, children=html_nodes)
        list_item_nodes.append(li_node)
    return list_item_nodes
