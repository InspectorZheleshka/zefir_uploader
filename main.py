from data import data_layer as storage
from os.path import join


def get_local_albums():
    return storage.get_albums_local()


def get_remote_albums():
    return storage.get_albums_remote()


def create_album(name, parent_id=None):
    return storage.create_album(name, parent_id)


def find_remote(remotes, name):
    if name is None:
        return None

    albums = [album for album in remotes if album['name'] == name]
    return albums[0] if len(albums) > 0 else None


def start_uploading(local_album, remote_album):
    pos = remote_album['total_nb_images']

    images = local_album['__content__']
    images_count = len(images)

    local_album_full_path = join(local_album['parent'], local_album['title'])

    while pos < images_count:
        image_to_upload = images[pos]

        upload_image(join(local_album_full_path, image_to_upload), remote_album['id'])

        pos += 1


def upload_image(image_path, cat_id):
    storage.upload_image(image_path, cat_id)


def main():
    local_albums = get_local_albums()
    remote_albums = get_remote_albums()

    print(local_albums)
    print(remote_albums)

    local_albums_titles = [alb['title'] for alb in local_albums]
    remote_albums_titles = [alb['name'] for alb in remote_albums]

    print(local_albums_titles)
    print(remote_albums_titles)

    for local_album in local_albums:
        title = local_album['title']

        if title not in remote_albums_titles:
            parent_p = local_album.get('parent_paths', [])
            parent_name = parent_p[-1] if len(parent_p) > 0 else None
            parent = find_remote(remote_albums, parent_name)
            parent_id = parent['id'] if parent is not None else None

            created_id = create_album(title, parent_id)
            new_remote = {'id': created_id, 'name': title, 'total_nb_images': 0}

            if parent_id is not None:
                new_remote['parent_id'] = parent_id

            remote_albums.append(new_remote)

        remote_album = find_remote(remote_albums, title)

        if remote_album['total_nb_images'] < len(local_album['__content__']):
            start_uploading(local_album, remote_album)


if __name__ == '__main__':
    main()
