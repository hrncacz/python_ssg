from enum import Enum


class TextType(Enum):
    TEXT = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, target):
        if self.text == target.text and self.text_type == target.text_type and self.url == target.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text.upper()}, {self.text_type.value.upper()}, {self.url.upper()})"
