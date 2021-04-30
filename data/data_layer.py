from api import uploader_api
from local_storage import local_storage

from os.path import join

api = uploader_api.Api()
api.login()


def get_albums_remote():
    albums = get_albums_for_cat()
    albums = flatten_remote_albums(albums)
    return albums


def get_albums_for_cat(parent_cat=None):
    albums = api.get_albums(parent_cat)

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
    albs = local_storage.get_local_albums()
    albs = flatten_local_albums(albs)
    albs = filter_local_albs(albs)
    return albs


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


def create_album(name):
    return api.create_album(name)
