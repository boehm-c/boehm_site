import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownBlocks(unittest.TestCase):
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

    def test_markdown_heading_3_block_type(self):
        block = "###"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.heading)

    def test_markdown_heading_6_block_type(self):
        block = "######"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.heading)

    def test_markdown_code_block_type(self):
        block = '```print("this is code")```'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.code)

    def test_markdown_quote_block_type(self):
        block = "> this is a quote block\n>with multiple lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.quote)

    def test_markdown_unordered_list_block_type(self):
        block = "- this is a\n- multi line\n- unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.unordered_list)

    def test_markdown_unordered_bad_list_block_type(self):
        block = "- this is a\n \n- multi line\n- unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)

    def test_markdown_ordered_list_block_type(self):
        block = "1. ordered list\n2. with three\n3. lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ordered_list)

    def test_markdown_paragraph_bad_ordered_list(self):
        block = "1. ordered list\n2. with three\n4. lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)

    def test_markdown_paragraph_bad_heading(self):
        block = "#######"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)
