import requests
from tqdm import tqdm
from http import HTTPStatus
from urllib.parse import urljoin
import configparser
import json


def main():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    vk_user = VK(config['VK']['vk_token'], config['VK']['user_id'])
    yadisk_user = YaDisk(config['YaDisk']['yadisk_token'])
    if vk_user.get_users_photos(config['VK']['user_id']):
        if yadisk_user.create_folder():
            print(f"Do you want to upload to '{yadisk_user.active_folder}' directory?")
            answer = input("[Y] - yes, [_] - cancel: ").upper()
            if answer == "Y":
                yadisk_user.upload_all_photos(vk_user, yadisk_user.active_folder)
            else:
                print("Uploading was cancelled")
        with open('photos_info.json', 'w') as file:
            json.dump(vk_user.photos_info, file)


if __name__ == '__main__':
    main()
