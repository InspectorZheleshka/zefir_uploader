from data import data_layer as storage


def get_local_albums():
    return storage.get_albums_local()


def get_remote_albums():
    return storage.get_albums_remote()


def main():
    local_albs = get_local_albums()
    remote_albums = get_remote_albums()

    print(local_albs)
    print(remote_albums)

    print([alb['title'] for alb in local_albs])
    print([alb['name'] for alb in remote_albums])


if __name__ == '__main__':
    main()
