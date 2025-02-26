import os
import shutil
import sys

from generator import copy_files_recursive, generate_pages_recursive


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <base_path>")
        sys.exit(1)

    base_path = sys.argv[1] if sys.argv[1] else "./"
    dir_path_static = os.path.join(base_path, "static")
    dir_path_public = os.path.join(base_path, "docs")
    dir_path_content = os.path.join(base_path, "content")
    template_path = os.path.join(base_path, "template.html")

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_public, base_path
    )


if __name__ == "__main__":
    main()
