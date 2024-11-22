import unittest
from enums import *
from textnode import *
from htmlnode import *
from splitter import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_notequal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node that aint", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == '__main__':
    unittest.main()
