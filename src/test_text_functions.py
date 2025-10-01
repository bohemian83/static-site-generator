import unittest
from textnode import TextNode
from text_functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        """Test basic code block splitting"""
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        """Test bold delimiter splitting"""
        node = TextNode("This is **bold** text", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")

        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        """Test italic delimiter splitting"""
        node = TextNode("This is *italic* text", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        """Test multiple occurrences of delimiter"""
        node = TextNode("This `code` and `more code` here", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [
            TextNode("This ", "text"),
            TextNode("code", "code"),
            TextNode(" and ", "text"),
            TextNode("more code", "code"),
            TextNode(" here", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        """Test node without delimiter remains unchanged"""
        node = TextNode("This is plain text", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [TextNode("This is plain text", "text")]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        """Test delimiter at the beginning"""
        node = TextNode("`code` at start", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [
            TextNode("code", "code"),
            TextNode(" at start", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        """Test delimiter at the end"""
        node = TextNode("End with `code`", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [
            TextNode("End with ", "text"),
            TextNode("code", "code"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_in_list(self):
        """Test splitting multiple nodes"""
        node1 = TextNode("First `code` here", "text")
        node2 = TextNode("Second `code` there", "text")
        new_nodes = split_nodes_delimiter([node1, node2], "`", "code")

        expected = [
            TextNode("First ", "text"),
            TextNode("code", "code"),
            TextNode(" here", "text"),
            TextNode("Second ", "text"),
            TextNode("code", "code"),
            TextNode(" there", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_type_unchanged(self):
        """Test that non-TEXT nodes are not split"""
        node = TextNode("already bold", "bold")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected = [TextNode("already bold", "bold")]
        self.assertEqual(new_nodes, expected)

    def test_mixed_node_types(self):
        """Test list with mixed node types"""
        node1 = TextNode("Text with `code`", "text")
        node2 = TextNode("Already bold", "bold")
        node3 = TextNode("More `code` here", "text")

        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", "code")

        expected = [
            TextNode("Text with ", "text"),
            TextNode("code", "code"),
            TextNode("Already bold", "bold"),
            TextNode("More ", "text"),
            TextNode("code", "code"),
            TextNode(" here", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_list(self):
        """Test empty list input"""
        new_nodes = split_nodes_delimiter([], "`", "code")
        self.assertEqual(new_nodes, [])

    def test_unclosed_delimiter_raises_error(self):
        """Test that unclosed delimiter raises an exception"""
        node = TextNode("Text with `unclosed delimiter", "text")

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", "code")


class TestExtractMarkdownImages(unittest.TestCase):
    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_single_image(self):
        text = "Check out this image: ![cat](https://example.com/cat.png)"
        expected = [("cat", "https://example.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This is just plain text with no images"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text(self):
        text = "![](https://example.com/image.jpg)"
        expected = [("", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_single_link(self):
        text = "Visit [Google](https://www.google.com) for search"
        expected = [("Google", "https://www.google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This is just plain text with no links"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_anchor_text(self):
        text = "[](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()
