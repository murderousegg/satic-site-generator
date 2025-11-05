import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_heading_levels_1_through_6(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Not a heading: no space after hashes
        self.assertEqual(block_to_block_type("###No space"), BlockType.PARAGRAPH)

    def test_code_block_fenced_with_backticks(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Not code: only starting backticks
        not_code = "```python\nprint('hello')"
        self.assertEqual(block_to_block_type(not_code), BlockType.PARAGRAPH)

    def test_quote_block_all_lines_start_with_gt(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Not a quote block: one line missing '>'
        mixed = "> line one\nnot quoted\n> line three"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_ordered_list_incrementing_and_unordered_list(self):
        # Valid ordered list: starts at 1 and increments by 1
        ordered = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ordered), BlockType.ORDERED_LIST)

        # Invalid ordered list: skips a number → should be paragraph
        bad_ordered = "1. first\n3. second\n4. third"
        self.assertEqual(block_to_block_type(bad_ordered), BlockType.PARAGRAPH)

        # Unordered list: every line starts with "- "
        unordered = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(unordered), BlockType.UNORDERED_LIST)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
        unittest.main()