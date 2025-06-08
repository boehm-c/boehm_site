from enum import Enum


class HTMLType(Enum):
    PARAGRAPH = "p"
    LINK = "a"
    HEADING = "h1"
    SPAN = "span"
    DIV = "div"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    IMAGE = "img"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = [] if children is None else children
        self.props = {} if props is None else props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        props_string = ""
        for prop in self.props:
            props_string += " " + prop + '="' + self.props[prop] + '"'
        return props_string

    def __eq__(self, html_node):
        if (
            self.tag == html_node.tag
            and self.value == html_node.value
            and self.children == html_node.children
            and self.props == html_node.props
        ):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf Node must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNodes must have tags")
        if not self.children:
            raise ValueError("ParentNodes must have children")
        new_text = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            new_text += node.to_html()
        return new_text + f"</{self.tag}>"
