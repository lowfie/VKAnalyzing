from data.config import VK_TOKEN
import requests

group_name = input('Введите название группы: ')


class VkParser:
    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.vk_version = 'v=5.131'

    def get_posts(self):
        link = self.url + f'wall.get?domain={group_name}&count=40&access_token={VK_TOKEN}&{self.vk_version}'
        response = requests.get(link)
        return response.text

    def get_wall_comments(self, owner_id, post_id):
        link = self.url + f'wall.getComments?owner_id={owner_id}&post_id={post_id}&count=100&sort=desc&access_token={VK_TOKEN}&{self.vk_version}'
        response = requests.get(link)
        return response.text

    def main(self):
        posts = self.get_posts()
        print(posts)


if __name__ == '__main__':
    vk_parser = VkParser()
    vk_parser.main()
