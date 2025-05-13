from enum import Enum


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
        self.text_type = text_type
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
