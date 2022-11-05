import requests
import json
from tqdm import tqdm
from pprint import pprint

vk_id = '51444562'
vk_token = '7d43790d7d43790d7d43790de07e53825f77d437d43790d1e02d420e2dd67baaa0a0426'
ya_token = ''
folder_name = input('Введите название папки на Яндекс Диске: ')


class Downloads_Photo:
    def __init__(self, vk_token: str, vk_id: str, version='5.131'):
        self.user_id = vk_id
        self.token_vk = vk_token
        self.version = version

    def downloads_photo_from_vk(self, album_id=input('Введите ID альбома: ')):
        params = {
            'owner_id': self.user_id,
            'album_id': album_id,
            'access_token': self.token_vk,
            'photo_sizes': 1,
            'extended': '1',
            'v': self.version
        }
        new_list = []
        new_dict = {}
        req = requests.get('https://api.vk.com/method/photos.get',params).json()
        all_photos = req['response']['items']
        for photo in all_photos:
            new_dict = {
                'file_name': f"{photo['likes']['count']}-{photo['date']}.jpg",
                'URL': photo['sizes'][-1]['url'],
                'size': photo['sizes'][-1]['type']
            }
            new_list.append(new_dict)
        pprint(new_list)
        with open('data.json', 'w') as outfile:
            json.dump(new_list, outfile, indent=0)
        return new_list


class Upload_Photo:
    def __init__(self, ya_token: str):
        self.token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def create_folder(self, folder_name):
        params = {
            'path': f'{folder_name}'
        }
        requests.put(self.url, headers=self.headers, params=params)

    def uploading_files_to_yandex_disk(self, folder_name):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for file in tqdm(data):
            for file in tqdm(data):
                params = {
                    'url': file['URL'],
                    'path': f"{folder_name}/{file['file_name']}"
                }
                response = requests.post(upload_url,
                                         params=params,
                                         headers=self.headers)
            response.raise_for_status()
            if response.status_code == 202:
                print('Фото успешно загружено на Яндекс Диск')


if __name__ == '__main__':
    user_vk = Downloads_Photo(vk_token, vk_id)
    data = user_vk.downloads_photo_from_vk()
    pprint(data)
    user_vk.downloads_photo_from_vk()
    user_ya = Upload_Photo(ya_token)
    user_ya.create_folder(folder_name)
    user_ya.uploading_files_to_yandex_disk(folder_name)