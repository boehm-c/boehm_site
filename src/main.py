from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("new text", "bold", "fake.url")
    print(text_node)


if __name__ == "__main__":
    main()
