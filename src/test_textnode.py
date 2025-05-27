import unittest

from textnode import TextNode, TextType
from markdown_blocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node no url", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_type_dif(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an image text node", TextType.IMAGE)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_has_url(self):
        node = TextNode("This text node has a url", TextType.CODE, ".com")
        self.assertTrue(node.url)


if __name__ == "__main__":
    unittest.main()
