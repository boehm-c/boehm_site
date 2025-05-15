import unittest

from textnode import TextNode, TextType
from convertnode import text_to_htmlnode, split_nodes_delimiter, extract_markdown_images


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a different text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node no url", TextType.BOLD_TEXT)
        self.assertEqual(node.url, None)

    def test_type_dif(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is an image text node", TextType.IMAGE_TEXT)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_has_url(self):
        node = TextNode("This text node has a url", TextType.CODE_TEXT, ".com")
        self.assertTrue(node.url)

    def test_text_to_htmlnode(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_htmlnode(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        html_node = text_to_htmlnode(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_split_bold_phrase(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.NORMAL_TEXT
        )
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("bolded phrase", TextType.BOLD_TEXT, None),
                TextNode(" in the middle", TextType.NORMAL_TEXT, None),
            ],
        )

    def test_split_bold_start_phrase(self):
        node = TextNode("**bolded phrase** at the start", TextType.NORMAL_TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(
            split_nodes,
            [
                TextNode("bolded phrase", TextType.BOLD_TEXT, None),
                TextNode(" at the start", TextType.NORMAL_TEXT, None),
            ],
        )

    def test_split_bold_end_phrase(self):
        node = TextNode("at the end **bolded phrase**", TextType.NORMAL_TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(
            split_nodes,
            [
                TextNode("at the end ", TextType.NORMAL_TEXT, None),
                TextNode("bolded phrase", TextType.BOLD_TEXT, None),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_images(
            "This is text with a ![link to boot.dev](https://www.boot.dev), and another to ![youtube.com](https://www.youtube.com)"
        )
        self.assertListEqual(
            [("link to boot.dev", "https://www.boot.dev"), ("youtube.com", "https://www.youtube.com")],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
