import os
import shutil

from textnode import TextNode, TextType
from generate_page import generate_page, generate_pages_recursive

def source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)

    copy_static_files(source, destination)

def copy_static_files(source, destination):
    items = os.listdir(source)

    for item in items:
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        if os.path.isfile(source_item):
            shutil.copy(source_item, destination_item)
            print(f"Copied {source_item} to {destination_item}")
        else:
            os.mkdir(destination_item)
            print(f"Created directory {destination_item}")
            copy_static_files(source_item, destination_item)

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    source_to_destination(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()