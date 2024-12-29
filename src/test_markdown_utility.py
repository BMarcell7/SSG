import unittest
from markdown_utility import *

class TestExtractTitle(unittest.TestCase):

    def test_valid_h1_header(self):
        markdown = "# Title of the page\nSome content here."
        self.assertEqual(extract_title(markdown), "Title of the page")

    def test_missing_h1_header(self):
        markdown = "This is a paragraph\nAnd another one."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
            
if __name__ == '__main__':
    unittest.main()