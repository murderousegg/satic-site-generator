import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_valid_tag_and_leaf_children(self):
        # Arrange
        c1 = LeafNode("b", "bold text")
        c2 = LeafNode("i", "italic text")
        parent = ParentNode("p", [c1, c2])

        # Act
        result = parent.to_html()

        # Assert
        expected = "<p>" + c1.to_html() + c2.to_html() + "</p>"
        self.assertEqual(result, expected)

    def test_to_html_raises_if_no_tag(self):
        c = LeafNode("span", "child text")
        node = ParentNode(None, [c])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html_preserves_child_order(self):
        c1 = LeafNode("a", "first")
        c2 = LeafNode("b", "second")
        c3 = LeafNode("c", "third")
        parent = ParentNode("div", [c1, c2, c3])
        result = parent.to_html()

        self.assertTrue(result.startswith("<div>"))
        self.assertTrue(result.endswith("</div>"))
        # Check that children are concatenated in order
        self.assertIn(c1.to_html() + c2.to_html() + c3.to_html(), result)
    

if __name__ == "__main__":
    unittest.main()