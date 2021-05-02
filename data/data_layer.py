from api import uploader_api
from local_storage import local_storage

from os.path import join, split

api = uploader_api.Api()
api.login()


def get_albums_remote():
    albums = get_albums_for_cat()

    if albums is None:
        input("Can't obtain remotes")
        exit()

    albums = flatten_remote_albums(albums)
    return albums


def get_albums_for_cat(parent_cat=None):
    albums = api.get_albums(parent_cat)

    if albums is None:
        return None

    if parent_cat is not None:
        pos = 0
        for item in albums:
            if item['id'] == parent_cat:
                break
            pos += 1

        if pos != len(albums):
            del albums[pos]

    for alb in albums:
        if alb['nb_categories'] > 0:
            alb['__content__'] = get_albums_for_cat(alb['id'])

            if len(alb['__content__']) == 0:
                del alb['__content__']

    return albums


def flatten_remote_albums(albums, parent=None):
    res = []

    for album in albums:
        content = album.get('__content__', None)

        if '__content__' in albums:
            del album['__content__']

        if parent is not None:
            album['parent_id'] = parent

        res.append(album)

        if content is not None:
            content = flatten_remote_albums(content, album['id'])
            res.extend(content)

    return res


def get_albums_local():
    albums = local_storage.get_local_albums()
    albums = flatten_local_albums(albums)
    albums = filter_local_albs(albums)
    albums = sort_local_albums(albums)
    albums = sort_images(albums)
    return albums


def flatten_local_albums(albums, title=local_storage.storage_path, path=None):
    res = []
    alb = dict()
    alb['parent'] = path
    alb['title'] = title

    for alb_title in albums:
        if alb_title == '__content__':
            alb['__content__'] = albums[alb_title]
        else:
            al_path = join(path, title) if path is not None else title
            res.extend(flatten_local_albums(albums[alb_title], title=alb_title, path=al_path))

    res.append(alb)

    return res


def filter_local_albs(albums):
    return [album for album in albums if len(album['__content__']) > 0]


def sort_local_albums(albums):
    for alb in albums:
        paths = split_path(alb['parent'])
        alb['parent_paths'] = paths

    return sorted(albums, key=lambda album: len(album['parent_paths']))


def sort_images(albums):
    for album in albums:
        content = album['__content__']
        album['__content__'] = sorted(content, key=name_to_int, reverse=False)
    return albums


def name_to_int(name):
    try:
        return int(name.split('.')[0])
    except Exception as ex:
        print(ex)
        return 99999999


def split_path(path):
    res = []

    if path is None or len(path) == 0:
        return res

    a, b = split(path)
    while len(a) > 0:
        res.append(b)
        a, b = split(a)

    return res


def create_album(name, parent_id=None):
    return api.create_album(name, parent_id)


def upload_image(image_path, cat_id):
    file = open(image_path, 'rb')
    return api.upload_image(file, cat_id, split(image_path)[1])
