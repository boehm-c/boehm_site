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
        if node.text_type != "normal" or node.text.count(delimiter) == 0:
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


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        markdown_images = extract_markdown_images(current_text)
        if not len(markdown_images):
            new_nodes.append(node)
        else:
            current_image = 0
            count_images = len(markdown_images)
            for image in markdown_images:
                current_image += 1
                sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE_TEXT, image[1]))
                if current_image == count_images and sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.NORMAL_TEXT))
                else:
                    current_text = sections[1]
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        markdown_links = extract_markdown_links(current_text)
        if not len(markdown_links):
            new_nodes.append(node)
        else:
            current_link = 0
            count_links = len(markdown_links)
            for link in markdown_links:
                current_link += 1
                sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK_TEXT, link[1]))
                if current_link == count_links and sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.NORMAL_TEXT))
                else:
                    current_text = sections[1]
    return new_nodes
