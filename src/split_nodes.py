from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown: unmatched delimiter")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_list.extend(split_nodes)
    return new_list
