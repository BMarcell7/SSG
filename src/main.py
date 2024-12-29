from textnode import *
import os
import shutil
from markdown_utility import *

    
def delete_contents_of_directory(directory):
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
        
            if os.path.isdir(item_path):
               delete_contents_of_directory(item_path)
               os.rmdir(item_path)
            else:
                os.remove(item_path)
    except Exception as e:
        print(f"Error occured while deleting contents of directory: {e}")
        
def copy_contents_of_directory(src, dest):
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        delete_contents_of_directory(dest)
        
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(src_path):
                copy_contents_of_directory(src_path, dest_path)
            else:
                shutil.copy(src_path, dest_path)
                print(f"Copied : {src_path} to {dest_path}")
    except Exception as e:
        print(f"Error occured while copying contents: {e}")
        
def main():
    node = TextNode("This is a text node", TextType.IMAGE, "Https.boot.com")
    print(node)

    content_dir = "content"
    public_dir = "public"
    template_path = "template.html"
    markdown_path = "content/index.md"
    generated_page_path = "public/index.html"
    
    delete_contents_of_directory(public_dir)
    copy_contents_of_directory("static", public_dir)
    
    generete_pages_recursive(content_dir, template_path, public_dir)
    
if __name__ == "__main__":
    main()