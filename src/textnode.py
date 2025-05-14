from enum import Enum
from htmlnode import LeafNode, HTMLType


class TextType(Enum):
    BOLD_TEXT = "bold"
    NORMAL_TEXT = "normal"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, text_node):
        if (
            self.text == text_node.text
            and self.text_type == text_node.text_type
            and self.url == text_node.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_to_htmlnode(self):
        if self.text_type == "normal":
            return LeafNode(tag=None, value=self.text)
        if self.text_type == "bold":
            return LeafNode(tag=HTMLType.BOLD, value=self.text)
        if self.text_type == "italic":
            return LeafNode(tag=HTMLType.ITALIC, value=self.text)
        if self.text_type == "code":
            return LeafNode(tag=HTMLType.CODE, value=self.text)
        if self.text_type == "link":
            props = {"href": self.url}
            return LeafNode(tag=HTMLType.LINK, value=self.text, props=props)
        if self.text_type == "image":
            props = {"src": self.url, "alt": self.text}
            return LeafNode(tag=HTMLType.IMAGE, props=props)
