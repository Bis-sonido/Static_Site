import unittest

from extract_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_text_nodes,
)

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is a link to [Google](https://www.google.com) and [GitHub](https://github.com)"
    )
    self.assertListEqual([
        ("Google", "https://www.google.com"),
        ("GitHub", "https://github.com"),
    ], 
    matches
    )

def test_extract_markdown_links_with_image(self):
    matches = extract_markdown_links(
        "This is a link to [Google](https://www.google.com) and an image ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([
        ("Google", "https://www.google.com"),
    ], 
    matches
    )

def test_extract_markdown_no_images(self):
    matches = extract_markdown_images(
        "This is text with no images."
    )
    self.assertListEqual([], matches)

def test_extract_markdown_no_links(self):
    matches = extract_markdown_links(
        "This is text with no links."
    )
    self.assertListEqual([], matches)

def test_split_images(self):
    node = TextNode(
        'This text with an image ![image](https://i.imgur.com/zjjcJKZ.png)', 
        TextType.IMAGE,
        )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is a text with an", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another", TextType.TEXT),
            TextNode( "Second Image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is a link to [Google](https://www.google.com) and [GitHub](https://github.com)", 
        TextType.LINK,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is a link to", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode("and", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ],
        new_nodes,
    )

def test_split_links_and_images(self):
    node = TextNode(
        "This is a link to [Google](https://www.google.com) and an image ![image](https://i.imgur.com/zjjcJKZ.png)", 
        [TextType.LINK, TextType.IMAGE],
    )
    new_nodes = split_nodes_link([node])
    new_nodes = split_nodes_image(new_nodes)
    self.assertListEqual(
        [
            TextNode("This is a link to", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode("and an image", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

def test_text_to_text_nodes(self):
    nodes = text_to_text_nodes(
        "This is **bold** text, *italic* text, `code` text, an image ![image](https://i.imgur.com/zjjcJKZ.png), and a link to [Google](https://www.google.com)."
    )
    self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text, an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(", and a link to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(".", TextType.TEXT),
        ],
        nodes,
    )


if __name__ == "__main__":
    unittest.main()
    