from api import uploader_api
from local_storage import local_storage

api = uploader_api.Api()
api.login()


def get_albums():
    return get_albums_for_cat()


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
        alb['__content__'] = get_albums_for_cat(alb['id'])

        if len(alb['__content__']) == 0:
            del alb['__content__']

    return albums


def get_albums_to_upload():
    return local_storage.get_local_albums()


def create_album(name):
    return api.create_album(name)
