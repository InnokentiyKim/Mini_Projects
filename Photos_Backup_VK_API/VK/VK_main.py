import requests
from http import HTTPStatus
from urllib.parse import urljoin
import json


class VK:

    def __init__(self, access_token: str, user_id: str, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.base_url = 'https://api.vk.com/method/'
        self.photos_info = {}

    def get_users_info(self) -> json:
        url  = urljoin(self.base_url, 'users.get')
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def _generate_photo_name(self, likes_count: int, date_: str, ext='.jpg') -> str:
        name = f"{likes_count}{ext}"
        if name in self.photos_info['names']:
            name = f"{likes_count}_{date_}{ext}"
        return name

    @staticmethod
    def _get_photos_amount():
        while True:
            try:
                amount = int(input("Enter photos amount: "))
                if amount > 0:
                    return amount
                else:
                    print("Количество должно быть больше 0")
            except:
                print("Введено не число")


    def get_users_photos(self, owner_id: str, album_id='profile') -> bool:
        url = urljoin(self.base_url, 'photos.get')
        photos_amount = self._get_photos_amount()
        params = {'owner_id': owner_id, 'album_id': album_id, 'rev': 0,
                  'extended': 1, 'photo_sizes': 1, 'count': photos_amount}
        try:
            response = requests.get(url, params={**self.params, **params})
        except requests.exceptions.ConnectionError:
            print('Connection error!')
            return False
        except Exception:
            print('Unexpected error occured!')
            return False
        if response.status_code == HTTPStatus.OK:
            all_info = None
            try:
                all_info = response.json()
                self.photos_info['count'] = 0
                self.photos_info['names'] = []
                self.photos_info['items'] = []
                for item in all_info['response']['items']:
                    item_info = {}
                    item_info['date'] = item['date']
                    item_info['likes_count'] = item['likes']['count']
                    sizes_urls = {item['sizes'][i]['type']: item['sizes'][i]['url'] for i in range(len(item['sizes']))}
                    max_size = max(sizes_urls.keys()) if 'w' not in sizes_urls else 'w'
                    item_info['size'] = max_size
                    item_info['url'] = sizes_urls[max_size]
                    self.photos_info['items'].append(item_info)
                    self.photos_info['count'] += 1
                    self.photos_info['names'].append(self._generate_photo_name(item_info['likes_count'], item_info['date']))
                return True
            except Exception:
                print(all_info['error']['error_msg'])
                return False
        return False
