import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="here is a value", props={"href": "url.com"})
        node2 = HTMLNode(tag="a", value="here is a value", props={"href": "url.com"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(
            tag="a",
            value="This is a link tag",
            props={"href": "url.com", "key2": "key2 value"},
        )
        node2 = HTMLNode(tag="p", value="This is a paragraph tag")
        self.assertNotEqual(node, node2)

    def test_none_value(self):
        node = HTMLNode(tag="h1")
        self.assertEqual(node.value, None)

    def test_has_url(self):
        node = HTMLNode(props={"href": "url.com"})
        self.assertTrue(node.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "url.com"})
        self.assertEqual(node.to_html(), '<a href="url.com">Hello, world!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
