import unittest
from helper import *

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
