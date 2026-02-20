import os
import shutil
from pathlib import Path
from markdown_blocks import markdown_to_html_nodes
from extract_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} to {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_nodes(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        content_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(content_item_path):
            dest_item_path = Path(dest_item_path).with_suffix(".html")
            generate_page(content_item_path, template_path, dest_item_path)
        elif os.path.isdir(content_item_path):
            generate_pages_recursive(content_item_path, template_path, dest_item_path)