from dotenv import load_dotenv
import requests
import random
import os

def get_image_extension(url):
    url_parts = url.split('.')
    return url_parts[-1]

def get_pic_information(pic_number):
    url = 'http://xkcd.com/{}/info.0.json'.format(pic_number)
    response = requests.get(url)
    image_information = response.json()
    return image_information

def download_pic(pic_number, download_url):
    extension = get_image_extension(download_url)
    filename = 'xkcd_{}.{}'.format(pic_number, extension)
    response = requests.get(download_url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename
    
def post_pic(access_token, owner_id, group_id, attachment_type, filename, message):
    attachments = get_params_for_safe_photo_on_wall(access_token, group_id, filename, attachment_type)
    payload = {'access_token': access_token,
             'v': 5.92,
             'owner_id': owner_id,
             'group_id':  group_id,
             'from_group': 1,
             'attachments': attachments,
             'message': message}
    
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    os.remove(filename)

def get_params_for_safe_photo_on_wall(access_token, group_id, filename, attachment_type):
    payload = {'access_token': access_token,
              'v': 5.92,
              'group_id':  group_id}
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    params_for_upload_xkcd = response.json()


    with open(filename, 'rb') as image_file_descriptor:
        files = {'photo': image_file_descriptor}
        url = params_for_upload_xkcd['response']['upload_url']
        response = requests.post(url, files=files)
        upload_information = response.json()
    
    photo_information = upload_information['photo']
    server_information = upload_information['server']
    hash_information = upload_information['hash']
    
    return get_information_for_post_on_wall(access_token, group_id, photo_information, server_information, hash_information, attachment_type)

def get_information_for_post_on_wall(access_token, group_id, photo_information, server_information, hash_information, attachment_type):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {'access_token': access_token,
             'v': 5.92,
             'photo': photo_information,
             'group_id':  group_id,
             'server': server_information,
             'hash': hash_information}
    response = requests.post(url, params=payload)
    saveWallPhoto_params = response.json()
    attachment_media_id = saveWallPhoto_params['response'][0]['id']
    attachment_owner_id = saveWallPhoto_params['response'][0]['owner_id']
    attachments = '{}{}_{}'.format(attachment_type, attachment_owner_id, attachment_media_id)
    
    return attachments

def main():
    load_dotenv()
    access_token = os.getenv("access_token")
    attachment_type = os.getenv("attachment_type")
    owner_id = os.getenv("owner_id")
    group_id = os.getenv("group_id")
    
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    last_pic_information = response.json()
    pic_number = random.randrange(1, last_pic_information['num'], 1)
    
    pic_information = get_pic_information(pic_number)
    message = pic_information['alt']
    download_url = pic_information['img']
    
    filename = download_pic(pic_number, download_url)
    post_pic(access_token, owner_id, group_id, attachment_type, filename, message)

if __name__ == '__main__':
    main()
