from os.path import join, isdir

from local_storage import utils

storage_path = 'cache'


def get_local_albums():
    main_content = utils.get_files(storage_path)
    return parse_paths(storage_path, main_content)


def parse_paths(path, files):
    result = {'__content__': []}

    for item in files:
        filepath = join(path, item)
        if isdir(filepath):
            nested_files = utils.get_files(filepath)
            result[item] = parse_paths(filepath, nested_files)
        else:
            result['__content__'].append(item)

    return result
