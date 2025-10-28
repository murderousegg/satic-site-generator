import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_with_tag_and_value(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_raises_if_no_value(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()
    

if __name__ == "__main__":
    unittest.main()