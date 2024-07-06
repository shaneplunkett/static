import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_html_props(self):
        node = HTMLNode("yolo", "howdy", None,
                        {"prop": "prop1", "href": "https://google.com.au"},
                        )
        self.assertEqual(node.props_to_html(), ' prop="prop1" href="https://google.com.au"',)
