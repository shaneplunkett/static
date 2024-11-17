from textnode import TextNode, TextType 

def main():

    node = TextNode("This is a Text Node", TextType.BOLD, "https://www.google.com")
    print(node)    

main()
