import shutil
import os


def list_folder_recursively(parent_path, current_folder):
    current_path = os.path.join(parent_path, current_folder)
    if not os.path.isdir(current_path):
        return None
    else:
        folder_dict = {}
        folder_content = os.listdir(current_path)
        for f in folder_content:
            folder_dict[f] = list_folder_recursively(current_path, f)
        return folder_dict


def delete_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public")


def copy_to_public(from_folder, to_folder, folder_dict):
    if not os.path.exists(to_folder):
        os.mkdir(to_folder)
    for fd in folder_dict.items():
        if isinstance(fd[1], dict):
            copy_to_public(os.path.join(from_folder, fd[0]), os.path.join(
                to_folder, fd[0]), fd[1])
        else:
            shutil.copy(os.path.join(
                from_folder, fd[0]), os.path.join(to_folder, fd[0]))


test = """

{
    static: {
        images: {
            tolkien.png: None
        },
        index.css: None
    }
}

"""
