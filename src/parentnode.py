from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError
        start_tag = f"<{self.tag}>"
        child_tags=""
        for child in self.children:
            child_tags+=child.to_html()
        end_tag = f"</{self.tag}>"
        return start_tag+child_tags+end_tag