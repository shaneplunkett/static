import unittest

from enums import TextType
from markdown import markdown_to_blocks
from splitter import split_nodes_image, split_nodes_link
from textnode import TextNode


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = (
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            ),
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        output = split_nodes_link(node)
        self.assertEqual(output, expected)

    def test_split_nodes_image(self):
        input = (
            TextNode(
                "This is text with an image ![alttext](image.png) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,
            ),
        )
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alttext", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        output = split_nodes_image(input)
        self.assertEqual(output, expected)


class TextBlockSplit(unittest.TestCase):
    def test_split_text_block(self):
        markdown = (
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
            "\n"
            "* This is the first list item in a list block"
            "\n"
            "* This is a list item"
            "\n"
            "* This is another list item"
            "\n"
            "\n"
            "\n"
        )
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        output = markdown_to_blocks(markdown)
        self.assertEqual(output, expected)
