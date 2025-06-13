from public_generator import generate_public
from page_generator import generate_pages_recursively
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Starting SSG")
    generate_public("./static", "./docs")
    generate_pages_recursively(
        "./content",  "./docs", "./template.html", basepath)


main()
