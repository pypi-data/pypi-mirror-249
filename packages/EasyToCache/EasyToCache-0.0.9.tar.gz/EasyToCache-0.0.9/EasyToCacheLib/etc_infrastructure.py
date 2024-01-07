import os
from EasyToCacheLib.json_exp import *


def get_relevant_path(path: str) -> str:
    index = path.rfind('/')
    index = 0 if index < 0 else index
    directory, json_file = path[:index], path[index:]
    if directory != "" and not os.path.isdir(directory):
        raise InvalidDirectoryPathError(f"Directory path \"{directory}\" is invalid.")

    index = json_file.rfind('.')
    index = 0 if index < 0 else index
    file_name, resolution = json_file[:index], json_file[index:]
    if len(file_name) == 0:
        raise InvalidFileNameError(f"File name \"{file_name}\" is invalid.")
    if resolution != ".json":
        raise FileResolutionMustBeJsonError(f"File resolution must be \".json\", not \"{resolution}\"")
    return path


def main():
    get_relevant_path("jaj.json")


if __name__ == "__main__":
    main()
