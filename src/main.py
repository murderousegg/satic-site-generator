import os
import shutil
from markdown_to_blocks import markdown_to_html_node, extract_title
import sys

def clear_directory(path: str) -> None:
    """
    Remove all contents of the given directory, but not the directory itself.
    """
    if not os.path.exists(path):
        return

    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path) or os.path.islink(full_path):
            print(f"Deleting file: {full_path}")
            os.remove(full_path)
        elif os.path.isdir(full_path):
            print(f"Deleting directory: {full_path}")
            shutil.rmtree(full_path)


def copy_recursive(src: str, dst: str) -> None:
    """
    Recursively copy all files and subdirectories from src to dst.
    """
    # Ensure destination directory exists
    os.makedirs(dst, exist_ok=True)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isdir(src_path):
            print(f"Creating directory: {dst_path}")
            os.makedirs(dst_path, exist_ok=True)
            copy_recursive(src_path, dst_path)  # recursive step
        else:
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)


def copy_static_to_public() -> None:
    """
    Clear the public directory, then recursively copy everything
    from static_dir into public_dir.
    """
    # Make sure destination directory exists, then clear its contents
    public_dir = "public"
    static_dir = "static"
    os.makedirs(public_dir, exist_ok=True)
    clear_directory(public_dir)

    # Recursively copy everything over
    copy_recursive(static_dir, public_dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as f:
        markdown = f.read()

    template = ""
    with open(template_path) as f:
        template = f.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    os.makedirs("/".join(dest_path.split("/")[:-1]), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath): 
    template = ""
    with open(template_path) as f:
        template = f.read()
    
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            # Recurse into subdirectories
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, dest_path, basepath)

        elif entry.endswith(".md"):
            with open(entry_path, encoding="utf-8") as f:
                markdown = f.read()

            # Convert markdown to HTML
            html = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace("href=\"/", f"href=\"{basepath}")
            template = template.replace("src=\"/", f"src=\"{basepath}")

            # Write to corresponding .html file in dest_dir_path
            html_name = os.path.splitext(entry)[0] + ".html"
            output_path = os.path.join(dest_dir_path, html_name)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(template)

            print(f"Generated {output_path}")

def main(basepath):
    copy_static_to_public()
    generate_pages_recursive(f"content/", f"template.html", f"docs/", basepath)

    



if __name__=="__main__":
    basepath = sys.argv[1]
    main(basepath)