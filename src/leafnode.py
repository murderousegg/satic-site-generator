from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"