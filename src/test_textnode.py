import unittest

from textnode import TextNode, TextType
from convertnode import (
    text_to_htmlnode,
    split_nodes_delimiter,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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

    def test_text_to_htmlnode(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_htmlnode(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_to_htmlnode(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_split_bold_phrase(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.NORMAL
        )
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL, None),
                TextNode("bolded phrase", TextType.BOLD, None),
                TextNode(" in the middle", TextType.NORMAL, None),
            ],
        )

    def test_split_bold_start_phrase(self):
        node = TextNode("**bolded phrase** at the start", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("bolded phrase", TextType.BOLD, None),
                TextNode(" at the start", TextType.NORMAL, None),
            ],
        )

    def test_split_bold_end_phrase(self):
        node = TextNode("at the end **bolded phrase**", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("at the end ", TextType.NORMAL, None),
                TextNode("bolded phrase", TextType.BOLD, None),
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
            [
                ("link to boot.dev", "https://www.boot.dev"),
                ("youtube.com", "https://www.youtube.com"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link to myspace](https://www.myspace.com) and another [link to facebook](https://www.facebook.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode(
                    "link to myspace", TextType.LINK, "https://www.myspace.com"
                ),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "link to facebook",
                    TextType.LINK,
                    "https://www.facebook.com",
                ),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "This is text without any links",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without any links", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_text_nodes(self):
        test_raw_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(test_raw_text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
