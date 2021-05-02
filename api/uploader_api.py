from json import dumps, loads
from xmltodict import parse
from requests import Session


class Api:
    def __init__(self):
        self.base_path = 'https://mellowzefir.art/ws.php?format={format}&method={method}'
        self.s = Session()

    def request(self, method, data_format='json', files=None, **kwargs):
        try:
            resp = self.get_response(method, data_format, files, **kwargs)

            if data_format == 'rest':
                resp = parse(resp.content)
                res_dict = loads(dumps(resp))
                print(res_dict)
                return res_dict
            else:
                json_resp = resp.json()
                print(json_resp)
                return json_resp
        except Exception as ex:
            print(ex)
            return None

    def get_response(self, method, data_format='json', files=None, retry_count=0, **kwargs):
        if retry_count == 3:
            return None

        url = self.base_path.format(format=data_format, method=method)

        def req():
            if files is None:
                return self.s.post(url, data=kwargs)
            else:
                return self.s.post(url, data=kwargs, files=files)

        resp = req()

        if resp.status_code == 404 or resp.status_code == 405 or resp.status_code == 401:
            if self.login():
                return self.get_response(method, data_format, files, retry_count + 1, **kwargs)
            else:
                return None

        return resp

    def login(self):
        print(f'Login')

        resp = self.s.post(
            self.base_path.format(format='json', method='pwg.session.login'),
            data={'username': 'admin', 'password': 'hrtrbny^&$%3wrg*9:9845#W'}
        )

        print(resp.headers)

        cookie = resp.headers.get('Set-Cookie', None)
        cookie = cookie.split(',')

        new_cookie = None

        for cook in cookie:
            if 'pwg_id' in cook:
                new_cookie = cook.split(';')[0].strip()
                self.s.headers.update({'Cookie': new_cookie})

        print(f'cookie {new_cookie}')

        return resp.status_code == 200

    def get_albums(self, parent_cat=None):
        if parent_cat is None:
            resp = self.request('pwg.categories.getList')
        else:
            resp = self.request('pwg.categories.getList', cat_id=parent_cat)

        try:
            return resp['result']['categories']
        except Exception as ex:
            print(ex)
            return None

    def create_album(self, name, parent_id=None):
        print(f'Create album request: {name} nested in {parent_id}')
        if parent_id is None:
            resp = self.request('pwg.categories.add', name=name)
        else:
            resp = self.request('pwg.categories.add', name=name, parent=parent_id)

        try:
            return resp['result']['id']
        except Exception as ex:
            print(ex)
            return None

    def upload_image(self, image, cat_id, name):
        return self.request('pwg.images.addSimple', files={'image': image}, name=name, category=cat_id)
