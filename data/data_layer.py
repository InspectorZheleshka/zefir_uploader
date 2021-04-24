from api import uploader_api

api = uploader_api.Api()
api.login()


def get_albums():
    return api.get_albums()

def get_albums_to_upload():



def create_album(name):
    return api.create_album(name)
