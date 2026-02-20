import unittest

from generate_page import generate_page
from extract_markdown import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# Hello World")
        self.assertEqual(actual, "Hello World")

    def test_generate_page(self):
        actual = extract_title("""
# This is a title
This is a content.
""")
        self.assertEqual(actual, "This is a title")
    
    def test_eq_long(self):
        actual = extract_title("""
# This is a title

this is some content.

of text.

- list 1
- list 2
""")
        self.assertEqual(actual, "This is a title")
    
    def test_none(self):
        try:
            extract_title(
                """
This is a content without title.
"""
            )
            self.fail("Expected ValueError")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()