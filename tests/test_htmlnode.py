import unittest
from htmlnode import HTMLNode, LeafNode


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