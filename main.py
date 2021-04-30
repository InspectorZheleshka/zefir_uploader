from data import data_layer as storage


def get_local_albums():
    return storage.get_albums_to_upload()


def get_remote_albums():
    return storage.get_albums()


def main():
    local_albs = get_local_albums()
    remote_albums = storage.get_albums()

    print(local_albs)
    print(remote_albums)


if __name__ == '__main__':
    main()
