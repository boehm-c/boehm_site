from htmlnode import HTMLNode, HTMLType, LeafNode, ParentNode
from textnode import TextNode, TextType
import re


def text_to_htmlnode(textnode):
    if textnode.text_type == "normal":
        return LeafNode(tag=None, value=textnode.text)
    if textnode.text_type == "bold":
        return LeafNode(tag=HTMLType.BOLD, value=textnode.text)
    if textnode.text_type == "italic":
        return LeafNode(tag=HTMLType.ITALIC, value=textnode.text)
    if textnode.text_type == "code":
        return LeafNode(tag=HTMLType.CODE, value=textnode.text)
    if textnode.text_type == "link":
        props = {"href": textnode.url}
        return LeafNode(tag=HTMLType.LINK, value=textnode.text, props=props)
    if textnode.text_type == "image":
        props = {"src": textnode.url, "alt": textnode.text}
        return LeafNode(tag=HTMLType.IMAGE, props=props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "normal":
            new_nodes.append(node)
        elif node.text.count(delimiter) == 0:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 > 0:
            print(node.text)
            raise Exception("This node is invalid markdown")
        else:
            parts = node.text.split(delimiter)
            for i in range(0, len(parts)):
                if i % 2 == 1:
                    new_nodes.append(TextNode(parts[i], text_type))
                elif i % 2 == 0 and parts[i] != "":
                    new_nodes.append(TextNode(parts[i], TextType.NORMAL_TEXT))
    return new_nodes
