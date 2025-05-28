from enum import Enum

BlockType = Enum(
    "BlockType",
    ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"],
)


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    clean_blocks = list(
        map(lambda block: block.strip().replace("\n", "\n"), new_blocks)
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
