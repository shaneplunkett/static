import unittest
from helper import *
from textnode import *
from htmlnode import *
from enums import *
import textwrap

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rickroll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rickroll", "https://i.imgur.com/aKaOqIh.gif")]
        images = extract_markdown_images(text)
        self.assertEqual(images, expected)


class TextExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is a url to a youtube video [youtube](https://www.youtube.com/watch?v=m7no4O-JKDA)"
        expected = [("youtube", "https://www.youtube.com/watch?v=m7no4O-JKDA")]
        url = extract_markdown_links(text)
        self.assertEqual(url, expected)

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT),
        expected = [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" and ", TextType.TEXT),
             TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            ]
        output = split_nodes_link(node)
        self.assertEqual(output, expected)

    def test_split_nodes_image(self):
        input = TextNode("This is text with an image ![alttext](image.png) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT),
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alttext", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        output = split_nodes_image(input)
        self.assertEqual(output,expected)

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
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        output = markdown_to_blocks(markdown)
        self.assertEqual(output,expected)

class TestBlockCheck(unittest.TestCase):
    def test_block_check_heading1(self):
        block = "# This is a heading 1"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING1) 
        
    def test_block_check_heading2(self):
        block = "## This is a heading 2"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING2)

    def test_block_check_heading3(self):
        block = "### This is a heading 3"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING3) 

    def test_block_check_heading4(self):
        block = "#### This is a heading 4"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING4) 

    def test_block_check_heading5(self):
        block = "##### This is a heading 5"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING5)

    def test_block_check_heading6(self):
        block = "###### This is a heading 6"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.HEADING6)

    def test_block_check_not_heading(self):
        block = "########### This is not a heading"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.PARAGRAPH)

    def test_block_check_code(self):
        block = "```this is code```"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.CODE) 

    def test_block_check_quote(self):
        block = "> this is a quote"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.QUOTE) 
        
    def test_block_check_unordered_list(self):
        block = """* this is a list item
        * this is another list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.UNORDERED_LIST)

    def test_block_check_unordered_list_fail(self):
        block = """* this is a list item
        this is not another list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.PARAGRAPH)
    
    def test_block_check_unordered_list2(self):
        block = """- this is a list item
        - this is another list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.UNORDERED_LIST)
        
    def test_block_check_unordered_list2_fail(self):
        block = """- this is a list item
        this is not another list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.PARAGRAPH)

    def test_block_check_ordered_list(self):
        block = """1. this is a list item
2. this is another list item
3. this is a third list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.ORDERED_LIST)

    def test_block_check_ordered_list_fail(self):
        block = """1. this is a list item
        2. this is another list item
        4. this is a third list item"""
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.PARAGRAPH)

    def test_block_check_paragraph(self):
        block = "this is a boring old paragraph"
        output = block_to_block_type(block)
        self.assertEqual(output, BlockType.PARAGRAPH)
