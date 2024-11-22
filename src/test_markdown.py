import unittest
from markdown import *
from splitter import *
from textnode import *
from htmlnode import *
from enums import BlockType

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
