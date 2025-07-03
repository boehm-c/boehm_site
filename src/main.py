from markdown_blocks import markdown_to_html_node, extract_title
from os import listdir, mkdir, makedirs
from os.path import isfile, join, dirname, exists, splitext
import shutil


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    document_contents = open(from_path).read()
    template_contents = open(template_path).read()
    document_html = markdown_to_html_node(document_contents).to_html()
    title = extract_title(document_contents)
    template_contents = template_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", document_html
    )
    dir_path = dirname(dest_path)
    makedirs(dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)
        f.close()


def copy_static_directory(public_dir, static_path):
    current_items = listdir(static_path)
    for dir_item in current_items:
        item_path = join(static_path, f"{dir_item}")
        new_item_path = join(public_dir, f"{dir_item}")
        if isfile(item_path):
            shutil.copy(item_path, new_item_path)
        else:
            mkdir(new_item_path)
            copy_static_directory(new_item_path, item_path)

def copy_content_directory(public_dir, content_path, template_file_path):
    current_items = listdir(content_path)
    for dir_item in current_items:
        item_path = join(content_path, f"{dir_item}")
        if isfile(item_path):
            file_name, file_ext = splitext(dir_item)
            new_item_path = join(public_dir, f"{file_name}.html")
            generate_page(item_path, template_file_path, new_item_path)
        else:
            new_item_path = join(public_dir, f"{dir_item}")
            mkdir(new_item_path)
            copy_content_directory(new_item_path, item_path, template_file_path)


def create_public_directory(public_dir):
    if exists(public_dir):
        shutil.rmtree(public_dir)
    mkdir(public_dir)


def main():
    current_dir_name = dirname(__file__)
    static_dir = join(current_dir_name, "../static")
    public_dir = join(current_dir_name, "../public")
    content_dir = join(current_dir_name, "../content")
    template_file_path = join(current_dir_name, "../template.html")

    create_public_directory(public_dir)
    copy_static_directory(public_dir, static_dir)
    copy_content_directory(public_dir, content_dir, template_file_path)


    # index_md_file_path = join(content_dir, "index.md")
    # index_html_file_path = join(public_dir, "index.html")



    # generate_page(index_md_file_path, template_file_path, index_html_file_path)


if __name__ == "__main__":
    main()
