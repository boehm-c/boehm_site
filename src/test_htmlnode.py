import unittest

from htmlnode import HTMLNode, HTMLType


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            tag=HTMLType.LINK, value="here is a value", props={"href": "url.com"}
        )
        node2 = HTMLNode(
            tag=HTMLType.LINK, value="here is a value", props={"href": "url.com"}
        )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(
            tag=HTMLType.LINK,
            value="This is a link tag",
            props={"href": "url.com", "key2": "key2 value"},
        )
        node2 = HTMLNode(tag=HTMLType.PARAGRAPH, value="This is a paragraph tag")
        self.assertNotEqual(node, node2)

    def test_none_value(self):
        node = HTMLNode(tag=HTMLType.HEADING)
        self.assertEqual(node.value, None)

    def test_has_url(self):
        node = HTMLNode(props={"href": "url.com"})
        self.assertTrue(node.props)


if __name__ == "__main__":
    unittest.main()
