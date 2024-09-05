import configparser


class Settings:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        self.vk_user_id = config['VK']['user_id']
        self.vk_token = config['VK']['vk_token']
        self.yadisk_token = config['YaDisk']['yadisk_token']

    @property
    def get_user_id(self):
        return self.vk_user_id

    @property
    def get_vk_token(self):
        return self.vk_token

    @property
    def get_yadisk_token(self):
        return self.yadisk_token

settings = Settings()
