import unittest

from textnode import TextNode, TextType


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
        html_node = node.text_to_htmlnode()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_htmlnode(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        html_node = node.text_to_htmlnode()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")


if __name__ == "__main__":
    unittest.main()
