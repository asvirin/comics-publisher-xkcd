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
url = 'https://api.vk.com/method/wall.post?access_token={}&v=5.92&owner_id={}&group_id={}&from_group=1&attachments={}&message={}'.format(access_token, owner_id, group_id, attachments, message)
response = requests.post(url)
os.remove(filename)

def get_params_for_safe_photo_on_wall(access_token, group_id, filename, attachment_type):
  url = 'https://api.vk.com/method/photos.getWallUploadServer?access_token={}&v=5.92&group_id={}'.format(access_token, group_id)
response = requests.get(url)
params_for_upload_xkcd = response.json()

image_file_descriptor = open(filename, 'rb')
files = {
  'photo': image_file_descriptor
}
url = params_for_upload_xkcd['response']['upload_url']

response = requests.post(url, files = files)
upload_information = response.json()
image_file_descriptor.close()

photo = upload_information['photo']
server = upload_information['server']
hash = upload_information['hash']

return get_information_for_post_on_wall(access_token, group_id, photo, server, hash, attachment_type)

def get_information_for_post_on_wall(access_token, group_id, photo, server, hash, attachment_type):
  url = 'https://api.vk.com/method/photos.saveWallPhoto?access_token={}&v=5.92&group_id={}&photo={}&server={}&hash={}'.format(access_token, group_id, photo, server, hash)

response = requests.post(url)
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
