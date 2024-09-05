from VK.VK_main import VK
from YaDisk.YaDisk_main import YaDisk
from settings.config import settings
import json


class User:
    def __init__(self):
        self.user_id = settings.vk_user_id
        self.vk_user = VK(settings.vk_token, self.user_id)
        self.yadisk_user = YaDisk(settings.yadisk_token)

    def reserve_all_photos(self):
        if self.vk_user.get_users_photos(self.user_id):
            if self.yadisk_user.create_folder():
                print(f"Do you want to upload to '{self.yadisk_user.active_folder}' directory?")
                answer = input("[Y] - yes, [_] - cancel: ").upper()
                if answer == "Y":
                    self.yadisk_user.upload_all_photos(self.vk_user, self.yadisk_user.active_folder)
                else:
                    print("Uploading was cancelled")
            with open('photos_info.json', 'w') as file:
                json.dump(self.vk_user.photos_info, file)
