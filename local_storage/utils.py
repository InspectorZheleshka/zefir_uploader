from os import listdir, path


def get_files(path):
    return listdir(path)


def is_dir(file):
    return path.isdir(file)
