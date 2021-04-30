from json import dumps, loads
from xmltodict import parse
from requests import Session


class Api:
    def __init__(self):
        self.base_path = 'https://mellowzefir.art/ws.php?format={format}&method={method}'
        self.s = Session()

    def request(self, method, data_format='json', **kwargs):
        try:
            url = self.base_path.format(format=data_format, method=method)

            resp = self.s.post(url, data=kwargs)

            if resp.status_code == 404 or resp.status_code == 405 or resp.status_code == 401:
                if self.login():
                    resp = self.s.post(url, data=kwargs)
                else:
                    return None

            if data_format == 'rest':
                resp = parse(resp.content)
                res_dict = loads(dumps(resp))
                #print(res_dict)
                return res_dict
            else:
                json_resp = resp.json()
                #print(json_resp)
                return json_resp
        except Exception as ex:
            print(ex)
            return None

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
        return resp['result']['categories']

    def create_album(self, name):
        resp = self.request('pwg.categories.add', name=name)
        return resp
