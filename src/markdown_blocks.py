from enum import Enum
from inline_markdown import text_to_textnodes, text_to_htmlnode, text_to_htmlnode
from htmlnode import ParentNode
from textnode import TextNode, TextType
import re

BlockType = Enum(
    "BlockType",
    ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"],
)


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    clean_blocks = list(
        filter(
            lambda block: block != "",
            map(lambda block: block.strip().replace("\n", "\n"), new_blocks),
        )
    )
    return clean_blocks


def block_to_block_type(markdown_block):
    space_split_block = markdown_block.split()
    newline_split_block = markdown_block.split("\n")
    quote_check = list(
        map(lambda line: True if line[0] == ">" else False, newline_split_block)
    )
    unordered_check = list(
        map(lambda line: True if line[0:2] == "- " else False, newline_split_block)
    )
    is_ordered = True
    for i in range(len(newline_split_block)):
        line_split = newline_split_block[i].split(". ")
        line = i + 1
        if line_split[0] != str(line):
            is_ordered = False

    if len(space_split_block[0]) <= 6 and space_split_block[0].count("#") == len(
        space_split_block[0]
    ):
        return BlockType.heading
    elif markdown_block[0:3] == "```" and markdown_block[-3:] == "```":
        return BlockType.code
    elif quote_check.count(False) == 0:
        return BlockType.quote
    elif unordered_check.count(False) == 0:
        return BlockType.unordered_list
    elif is_ordered:
        return BlockType.ordered_list
    return BlockType.paragraph


def markdown_paragraph_to_html(block):
    p_leafs = list(map(lambda leaf: text_to_htmlnode(leaf), text_to_textnodes(block)))
    return ParentNode(tag="p", children=p_leafs)


def markdown_quote_to_html(block):
    quote_indent = 1
    quote_list_items = block.split("\n")
    child_text = []
    for li in quote_list_items:
        match = len(re.match(r"^\s*(>+)", li).group(1))
        text = li[match:].strip()
        child_text.append(text)
    p_leafs = list(
        map(
            lambda leaf: text_to_htmlnode(leaf), text_to_textnodes(" ".join(child_text))
        )
    )
    return ParentNode(tag="blockquote", children=p_leafs)


def markdown_heading_to_html(block):
    split_block = block.split(" ", 1)
    heading_tag = f"h{len(split_block[0])}"
    p_leafs = list(
        map(lambda leaf: text_to_htmlnode(leaf), text_to_textnodes(split_block[1]))
    )
    return ParentNode(tag=heading_tag, children=p_leafs)


def markdown_uol_to_html(block):
    """
    1. create leaf node text types
    2. create parent node list item
    3. create parent node unordered list
    """
    block_list_items = block.split("\n")
    html_list_items = []
    for li in block_list_items:
        li_leafs = list(
            map(lambda leaf: text_to_htmlnode(leaf), text_to_textnodes(li[2:]))
        )
        html_list_items.append(ParentNode(tag="li", children=li_leafs))
    return ParentNode(tag="ul", children=html_list_items)


def markdown_ol_to_html(block):
    """
    1. create leaf node text types
    2. create parent node list item
    3. create parent node unordered list
    """
    ordered_list_items = block.split("\n")
    html_list_items = []

    for i in range(len(ordered_list_items)):
        clean_item = ordered_list_items[i].split(f"{str(i+1)}. ", 1)[1]
        li_leafs = list(
            map(lambda leaf: text_to_htmlnode(leaf), text_to_textnodes(clean_item))
        )
        html_list_items.append(ParentNode(tag="li", children=li_leafs))
    return ParentNode(tag="ol", children=html_list_items)


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type.name == "paragraph":
            html_nodes.append(markdown_paragraph_to_html(block))
        if block_type.name == "unordered_list":
            html_nodes.append(markdown_uol_to_html(block))
        if block_type.name == "ordered_list":
            html_nodes.append(markdown_ol_to_html(block))
        if block_type.name == "code":
            stripped_block = block.replace("```", "")
            code_node = [text_to_htmlnode(TextNode(stripped_block, TextType.CODE))]
            html_nodes.append(ParentNode(tag="pre", children=code_node))
        if block_type.name == "quote":
            html_nodes.append(markdown_quote_to_html(block))
        if block_type.name == "heading":
            html_nodes.append(markdown_heading_to_html(block))
    div_node = ParentNode(tag="div", children=html_nodes)
    return div_node
