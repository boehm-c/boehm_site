from enum import Enum


class HTMLType(Enum):
    PARAGRAPH = "p"
    LINK = "a"
    HEADING = "h1"


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
