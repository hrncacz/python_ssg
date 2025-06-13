from public_generator import list_folder_recursively
from rawtext_tools import markdown_to_html, markdown_to_blocks
import os


def extract_title(blocks):
    title = ""
    filtered = list(filter(lambda l: l.startswith("# "), blocks))
    if len(filtered) > 0:
        title = filtered[0].replace("#", " ").strip()
    else:
        title = "Generic title"
    return title


def generate_md_to_html(from_path, dest_path, template_path, basepath):
    template_html = ""
    markdown = ""
    with open(template_path, "r", encoding="utf-8") as template_bytes:
        template_html = template_bytes.read()
    with open(from_path, "r", encoding="utf-8") as markdown_bytes:
        markdown = markdown_bytes.read()
    title = extract_title(markdown_to_blocks(markdown))
    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace(
        "{{ Content }}", markdown_to_html(markdown).to_html())
    template_html = template_html.replace("href=\"/", f"href=\"{basepath}")
    template_html = template_html.replace("src=\"/", f"src=\"{basepath}")
    with open(dest_path, "w", encoding="utf-8") as dest:
        dest.write(template_html)


def generate_to_public(from_folder, to_folder, folder_dict, template_path, basepath):
    if not os.path.exists(to_folder):
        print(f"- creating directory - {to_folder}")
        os.mkdir(to_folder)
    for fd in folder_dict.items():
        if isinstance(fd[1], dict):
            generate_to_public(os.path.join(from_folder, fd[0]), os.path.join(
                to_folder, fd[0]), fd[1], template_path, basepath)
        else:
            print(f"- generating HTML from - {os.path.join(
                from_folder, fd[0])}")
            generate_md_to_html(os.path.join(
                from_folder, fd[0]), os.path.join(to_folder, fd[0].replace(".md", ".html")), template_path, basepath)


def generate_pages_recursively(from_folder, to_folder, template_path, basepath):
    print("-----GENERATE HTML FILES-----")
    print(f"---Reading {from_folder}---")
    from_folder_arr = from_folder.split("/")
    folder_dict = list_folder_recursively(
        "/".join(from_folder_arr[:len(from_folder_arr)-1]), from_folder_arr[-1])
    print("---Starting to copy files---")
    generate_to_public(from_folder, to_folder, folder_dict,
                       template_path, basepath)
