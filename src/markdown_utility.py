from markdown_block import markdown_to_html_node
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception ("There is no Title")

def generate_page(from_path, template_path, dest_path):
    try:
        print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
        
        with open(from_path, "r") as md_file:
            markdown_content = md_file.read()
        
        title = extract_title(markdown_content)
        
        html_content = markdown_to_html_node(markdown_content).to_html()
        
        with open(template_path, "r") as template_file:
            template_content = template_file.read()
            
        full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
        
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        with open(dest_path, "w") as dest_file:
            dest_file.write(full_html)
            
        print(f"Page generated and saved to {dest_path}")
        
    except Exception as e:
        print(f"Error generating page: {e}")
        
def generete_pages_recursive(dir_path_content, template_path, dest_dir_path):
    try:
        for root, dirs, files in os.walk(dir_path_content):
            for file in files:
                if file.endswith(".md"):  # Check if it's a markdown file
                    markdown_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(markdown_file_path, dir_path_content)

                    # Build the destination path in the public directory
                    dest_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))

                    # Generate the page
                    generate_page(markdown_file_path, template_path, dest_path)
                    print(f"Page generated: {dest_path}")
    except Exception as e:
        print(f"Error generating pages recursively: {e}")