from textnode import TextNode
from public_generator import list_folder_recursively, delete_public, copy_to_public


def main():
    test_t = TextNode("This is some anchor text",
                      "link", "https://www.boot.dev")
    delete_public()
    copy_to_public("./static", "./public",
                   list_folder_recursively(".", "static"))


main()
