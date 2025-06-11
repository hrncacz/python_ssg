import unittest

from rawtext_tools import markdown_to_blocks, block_to_block_type, markdown_to_html


class TestRawTextTools(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
*** Header 3

* Header 1

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

1. This is a list
20. with items

```
To bych vynechala
Aj ta kuna
```







- Unordered list item 1
- and iitem 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "*** Header 3",
                "* Header 1",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "1. This is a list\n20. with items",
                "```\nTo bych vynechala\nAj ta kuna\n```",
                "- Unordered list item 1\n- and iitem 2"
            ],
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
