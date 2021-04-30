from data import data_layer as storage


def get_local_albums():
    return storage.get_albums_local()


def get_remote_albums():
    return storage.get_albums_remote()


def main():
    local_albums = get_local_albums()
    remote_albums = get_remote_albums()

    local_albums_titles = [alb['title'] for alb in local_albums]
    remote_albums_titles = [alb['title'] for alb in local_albums]

    print(local_albums)
    print(remote_albums)

    print(local_albums_titles)
    print(remote_albums_titles)


if __name__ == '__main__':
    main()
