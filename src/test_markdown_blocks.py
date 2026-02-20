import unittest

from extract_markdown import extract_title

from markdown_blocks import (
    markdown_to_blocks, 
    block_to_block_type,
    BlockType,
    markdown_to_html_nodes,
    block_to_html_node,
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_newlines(self):
        markdown = """
this is bolded paragraph

this is another paragraph with _italic_ text and `code` here
this is the same paragraph on a new line

- this is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "this is bolded paragraph",
                "this is another paragraph with _italic_ text and `code` here\nthis is the same paragraph on a new line",
                "- this is a list\n- with items",
            ],
        )

    def block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def block_to_block_type_code(self):
        block = "```python\nprint('Hello, world!')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def block_to_block_type_unordered_list(self):
        block = "- This is an unordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def block_to_block_type_ordered_list(self):
        block = "1. list item \n2. list item 2"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_unordered_list(self):
        md = """
- This is a list
- with items
"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li></ul></div>",
        )   
    
    def test_ordered_list(self):
        md = """
1. list item
2. list item 2
"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list item</li><li>list item 2</li></ol></div>",
        )  
    def test_quote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
             "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
    
    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_extract_title(self):
        md = """
# This is the title

"""
        node = extract_title(md)
        self.assertEqual(
            node,
            "This is the title",
        )
    

if __name__ == "__main__":
    unittest.main()