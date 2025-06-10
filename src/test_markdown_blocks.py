import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)


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

    def test_get_markdown_title(self):
        md = """
# This is a heading line
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a heading line")

    def test_extract_title_exception(self):
        md = """
There is no heading line
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue('Markdown Files should contain a title' in str(context.exception))

    def test_markdown_to_html_nodes(self):
        self.maxDiff = None
        md = """
## This is a heading 2 with **bold** text

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

- list item _1_
- list item **2**

1. ordered **list item 1**
2. ordered list item 2
3. ordered list item ```code``` 3

```
here is some sick code;
```

> The character of a > man is **what** he does _when_ no one is looking 
>> New quote line

a person

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading 2 with <b>bold</b> text</h2><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><ul><li>list item <i>1</i></li><li>list item <b>2</b></li></ul><ol><li>ordered <b>list item 1</b></li><li>ordered list item 2</li><li>ordered list item <code>code</code> 3</li></ol><pre><code>\nhere is some sick code;\n</code></pre><blockquote>The character of a > man is <b>what</b> he does <i>when</i> no one is looking New quote line</blockquote><p>a person</p></div>",
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
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
