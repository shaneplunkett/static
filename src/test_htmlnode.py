import unittest
from htmlnode import HTMLNode, LeafNode, text_node_to_html_node
from textnode import TextNode
from enums import *

class TestHTMLNode(unittest.TestCase):
    def test_html_props(self):
        node = HTMLNode("yolo", "howdy", None,
                        {"prop": "prop1", "href": "https://google.com.au"},
                        )
        self.assertEqual(node.props_to_html(), ' prop="prop1" href="https://google.com.au"',)

class TestLeafNode(unittest.TestCase):
    def test_leaf_values(self):
        node = LeafNode("p", "this is a paragraph of text")
        self.assertEqual(node.to_html(), '<p>this is a paragraph of text</p>')

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_conversion(self):
        text = "this is a paragraph of text"
        text_node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, text)

    def test_bold_type_conversion(self):
        text = "this is a paragraph of text"
        text_node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.tag, "b")

    def test_italic_type_conversion(self):
        text = "this is a paragraph of text"
        text_node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.tag, "i")

    def test_code_type_conversion(self):
        text = "this is a paragraph of code"
        text_node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.tag, "code")
    
    def test_link_type_conversion(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image_type_conversion(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


if __name__ == '__main__':
    unittest.main()

