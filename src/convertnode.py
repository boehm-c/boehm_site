from htmlnode import HTMLNode, HTMLType, LeafNode, ParentNode
from textnode import TextNode, TextType
import re


def text_to_htmlnode(textnode):
    if textnode.text_type == TextType.NORMAL:
        return LeafNode(tag=None, value=textnode.text)
    if textnode.text_type == TextType.BOLD:
        return LeafNode(tag=HTMLType.BOLD, value=textnode.text)
    if textnode.text_type == TextType.ITALIC:
        return LeafNode(tag=HTMLType.ITALIC, value=textnode.text)
    if textnode.text_type == TextType.CODE:
        return LeafNode(tag=HTMLType.CODE, value=textnode.text)
    if textnode.text_type == TextType.LINK:
        props = {"href": textnode.url}
        return LeafNode(tag=HTMLType.LINK, value=textnode.text, props=props)
    if textnode.text_type == TextType.IMAGE:
        props = {"src": textnode.url, "alt": textnode.text}
        return LeafNode(tag=HTMLType.IMAGE, props=props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL or node.text.count(delimiter) == 0:
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
                    new_nodes.append(TextNode(parts[i], TextType.NORMAL))
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
        if markdown_images:
            while markdown_images:
                image = markdown_images.pop(0)
                sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], node.text_type))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = sections[1]
            if current_text:
                new_nodes.append(TextNode(current_text, node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        markdown_links = extract_markdown_links(current_text)
        if markdown_links:
            while markdown_links:
                link = markdown_links.pop(0)
                sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], node.text_type))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = sections[1]
            if current_text:
                new_nodes.append(TextNode(current_text, node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(raw_text):
    node = TextNode(raw_text, TextType.NORMAL)
    nodes = [node]
    split_bold_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    split_italic_nodes = split_nodes_delimiter(split_bold_nodes, "_", TextType.ITALIC)
    split_code_nodes = split_nodes_delimiter(split_italic_nodes, "`", TextType.CODE)
    split_image_nodes = split_nodes_image(split_code_nodes)
    split_link_nodes = split_nodes_link(split_image_nodes)
    return(split_link_nodes)


# raw_text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
# new_nodes = text_to_textnodes(raw_text)
# print(new_nodes)
