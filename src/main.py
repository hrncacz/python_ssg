from textnode import TextNode
from public_generator import generate_public
from page_generator import generate_pages_recursively


def main():
    print("Starting SSG")
    generate_public("./static", "./public")
    generate_pages_recursively("./content",  "./public", "./template.html")


main()
