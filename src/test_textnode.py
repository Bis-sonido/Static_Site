import unittest

from textnode import TextNode, TextType
from node_to_html import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #personal test#1
    def test_neq(self): 
        my_node = TextNode("i'm italic", TextType.ITALIC)
        my_node2 = TextNode("i'm not italic", TextType.BOLD)
        self.assertNotEqual(my_node, my_node2)

    #personal test#2
    def test_image_eq(self):
        image_node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.png")
        image_node2 = TextNode("Image description", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(image_node, image_node2)
    
    #personal test#3
    def test_code_neq(self):
        code_node = TextNode("print('I'm code')", TextType.CODE)
        code_node2 = TextNode("print('I'm not code')", TextType.LINK)
        self.assertNotEqual(code_node, code_node2)

    #personal test#4
    def test_url_none(self):
        url_node = TextNode("this is a link", TextType.LINK)
        self.assertIsNone(url_node.url)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is bold")

    def test_italic(self):
        node = TextNode("this is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is italic")
    def test_code(self):
        node = TextNode("print(Hello, world)", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(Hello, world)")
    
    def test_link(self):
        node = TextNode("this is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Image description"})

if __name__ == "__main__":
    unittest.main()