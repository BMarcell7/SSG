from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children= None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError
        super().__init__(tag=tag, value=value, children= [], props=props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        
        if self.tag == "img":
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>"
        
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if not tag:
            raise ValueError ("This must have a tag")
        if not children:
            raise ValueError ("This must have a children")
        
        super().__init__(tag=tag, value=None, children=children, props= props)
      
    def to_html(self):
        
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    

def text_node_to_html_node(text_node):
    if text_node["type"] == TextType.TEXT:
        return LeafNode(None, text_node["content"])
    elif text_node["type"] == TextType.BOLD:
        return LeafNode("b", text_node["content"])
    elif text_node["type"] == TextType.ITALIC:
        return LeafNode("i", text_node["content"])
    elif text_node["type"] == TextType.CODE:
        return LeafNode("code", text_node["content"])
    elif text_node["type"] == TextType.LINK:
        if "href" not in text_node:
            raise ValueError("LINK type must have an 'href' attribute")
        return LeafNode("a", text_node["content"], {"href": text_node["href"]})
    elif text_node["type"] == TextType.IMAGE:
        if "src" not in text_node or "alt" not in text_node:
            raise ValueError("IMAGE type must have both 'src' and 'alt' attributes")
        return LeafNode("img", "", {"src": text_node["src"], "alt": text_node["alt"]})
    else:
        raise ValueError(f"Unknown TextType: {text_node['type']}")
