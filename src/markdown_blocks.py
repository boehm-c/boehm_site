def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    clean_blocks = list(
        map(lambda block: block.strip().replace("\n", "\n"), new_blocks)
    )
    return clean_blocks
