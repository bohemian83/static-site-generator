import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        node3 = TextNode(
            "This is another text node, with a different text", TextType.BOLD
        )
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)


if __name__ == "__main__":
    unittest.main()
