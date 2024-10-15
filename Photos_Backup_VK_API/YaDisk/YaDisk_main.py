from urllib.parse import urljoin
import requests
from tqdm import tqdm
from http import HTTPStatus
from VK.VK_main import VK


class YaDisk:

    def __init__(self, access_token: str, version='v1'):
        self.token = access_token
        self.version = version
        self.base_url = 'https://cloud-api.yandex.net'
        self.active_folder = 'New_Folder'

    @staticmethod
    def _get_folder_name():
        folder_name = input('Enter folder name: ')
        return folder_name.replace('/', '')

    def create_folder(self) -> bool:
        url = urljoin(self.base_url, f'{self.version}/disk/resources')
        folder_name = self._get_folder_name()
        headers = {'Authorization': self.token}
        params = {'path': folder_name}
        try:
            response = requests.put(url, params=params, headers=headers)
        except:
            print('Error occured!')
            return False
        if response.status_code == HTTPStatus.CREATED:
            print('Folder successfully created!')
            self.active_folder = folder_name
            return True
        elif response.status_code == HTTPStatus.CONFLICT:
            self.active_folder = folder_name
            print("Folder already exist")
            return True
        print('Folder creation failed!')
        print(response.json()['description'])
        return False

    def upload_photo(self, photo_url: str, disk_path: str) -> bool:
        disk_url = self.base_url + f'/{self.version}/disk/resources/upload'
        headers = {'Authorization': self.token}
        params = {'url': photo_url ,'path': disk_path, 'disable_redirects': 'false'}
        try:
            response = requests.post(disk_url, params=params, headers=headers)
        except:
            print('Uploading failed!')
            return False
        if response.status_code == HTTPStatus.ACCEPTED:
            return True
        return False

    def upload_all_photos(self, vk_user, folder_name: str) -> int:
        uploaded_files = 0
        if isinstance(vk_user, VK):
            photos_count = vk_user.photos_info['count']
            photo_links = [item['url'] for item in vk_user.photos_info['items']]
            print('Uploading files to yandex disk...')
            for i in tqdm(range(photos_count), colour='Green'):
                disk_path = folder_name + '/' + vk_user.photos_info['names'][i]
                if self.upload_photo(photo_links[i], disk_path):
                    uploaded_files += 1
            print('Done!')
            print('Number of uploaded files:', uploaded_files, '/', photos_count)
        return uploaded_files

