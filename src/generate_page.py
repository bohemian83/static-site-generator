import os
import shutil
from markdown_functions import markdown_to_html_node


def delete_contents(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for item in os.listdir(dest):
        item_path = os.path.join(dest, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path):
            os.remove(item_path)


def copy_assets(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_assets(src_path, dest_path)
        elif os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)


def move_assets(src, dest):
    delete_contents(dest)
    copy_assets(src, dest)


def extract_title(markdown):
    first_line = markdown.split("\n")[0]
    hash_count = first_line.count("#")
    if hash_count == 0:
        raise Exception("h1 header missing")
    elif hash_count > 1:
        raise Exception("Header contains more than one # characters")
    else:
        return first_line.strip("#").strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as mk:
        markdown = mk.read()
        title = extract_title(markdown)
        html = markdown_to_html_node(markdown).to_html()

    with open(template_path, "r") as tmpl:
        template = tmpl.read()
        index = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest:
        dest.write(index)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path)
        elif os.path.isfile(src_path):
            dest_filename = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_filename)
            generate_page(src_path, template_path, dest_path)
