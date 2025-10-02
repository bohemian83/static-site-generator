import unittest
from textnode import TextNode, TextType
from text_functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        """Test basic code block splitting"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        """Test bold delimiter splitting"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        """Test italic delimiter splitting"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        """Test multiple occurrences of delimiter"""
        node = TextNode("This `code` and `more code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        """Test node without delimiter remains unchanged"""
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        """Test delimiter at the beginning"""
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        """Test delimiter at the end"""
        node = TextNode("End with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_in_list(self):
        """Test splitting multiple nodes"""
        node1 = TextNode("First `code` here", TextType.TEXT)
        node2 = TextNode("Second `code` there", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" there", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_type_unchanged(self):
        """Test that non-TEXT nodes are not split"""
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_mixed_node_types(self):
        """Test list with mixed node types"""
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("More `code` here", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)

        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_list(self):
        """Test empty list input"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_unclosed_delimiter_raises_error(self):
        """Test that unclosed delimiter raises an exception"""
        node = TextNode("Text with `unclosed delimiter", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


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


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is text with an image ![alt text](https://example.com/image.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_images(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_surrounded_by_text(self):
        node = TextNode(
            "Text before ![image](https://example.com/pic.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_images(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](https://example.com/1.png)", TextType.TEXT),
            TextNode("Second ![img2](https://example.com/2.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_at_start(self):
        node = TextNode(
            "[First link](https://example.com) then some text", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("First link", TextType.LINK, "https://example.com"),
            TextNode(" then some text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_at_end(self):
        node = TextNode(
            "Some text then [last link](https://example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Some text then ", TextType.TEXT),
            TextNode("last link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_links(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](https://example.com/1)", TextType.TEXT),
            TextNode("Second [link2](https://example.com/2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
