import time

from data.config import VK_TOKEN
import requests

from database.models import Post, Comment, create_db
from loader import session

group_name = input('Введите название группы: ')


class VkParser:
    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.vk_version = 'v=5.131'
        self.posts = []

    def get_posts(self):
        link = self.url + f'wall.get?domain={group_name}&count=40&access_token={VK_TOKEN}&{self.vk_version}'
        response = requests.get(link).json()
        items = [item for item in response['response']['items']]

        for item in items:
            self.posts.append({'post_id': item['id'], 'owner_id': item['owner_id']})

            # post = Post(
            #     post_id=item['id'],
            #     owner_id=item['owner_id'],
            #     group=group_name,
            #     quantity_comments=item['comments']['count'],
            #     likes=item['likes']['count'],
            #     views=item['views']['count'],
            #     photo=True,
            #     post_text=item['text']
            # )
            # '''Когда ставлю autocommit=True, данные всё равно не сохраняются в бд'''
            # session.add(post)
            # session.commit()

    def get_wall_comments(self):
        for num, post in enumerate(self.posts, start=1):
            link = self.url + f'wall.getComments?owner_id={post["owner_id"]}&post_id={post["post_id"]}&count=100&sort=desc&access_token={VK_TOKEN}&{self.vk_version}'
            response = requests.get(link).json()
            if num % 5 == 0:
                time.sleep(2)

            for item in response['response']['items']:
                print(item['text'])

                # comment = Comment(
                #     comment_id=item['id'],
                #     post_id=post['post_id'],
                #     text=item['text']
                # )
                # session.add(comment)
                # session.commit()

    def main(self):
        self.get_posts()
        self.get_wall_comments()


if __name__ == '__main__':
    create_db()
    vk_parser = VkParser()
    vk_parser.main()
