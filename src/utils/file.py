import os


def create_parent_dir(file_path: str) -> None:
    file_directory = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(file_directory, exist_ok=True)
