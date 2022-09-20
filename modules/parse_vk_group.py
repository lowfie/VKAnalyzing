from data.config import VK_TOKEN
import httpx

from database.models import Post, Comment, create_tables
from database import Service
from loader import session

group_name = input('Введите название группы: ')


class VkParser:
    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.vk_version = 'v=5.131'
        self.posts_metadata = []

    def get_posts(self):
        """
        Парсинг данных 40 последних постов из группы вк
        И занесение данных в бд
        """
        link = self.url + f'wall.get?domain={group_name}&count=40&access_token={VK_TOKEN}&{self.vk_version}'
        response = httpx.get(link).json()

        # Список из 40 последних постов
        items = [item for item in response['response']['items']]

        for item in items:
            self.posts_metadata.append({'post_id': item['id'], 'owner_id': item['owner_id']})
            # Добавление данных в бд
            # Попробовать добавить bulk_insert_mappings (Оптимизация)
            post_data = {
                'id': item['id'],
                'owner_id': item['owner_id'],
                'group': group_name,
                'quantity_comments': item['comments']['count'],
                'likes': item['likes']['count'],
                'views': item['views']['count'],
                'photo': True if 'attachments' in item else False,
                'text': item['text']
            }
            if session.query(Post).filter(Post.post_id == post_data['id']).first() is None:
                Service.add_post(post_data)
            else:
                Service.update_post(post_data)

    def get_wall_comments(self):
        """
        Парсинг комментариев поста
        И занесение данных в бд
        """
        for num, post in enumerate(self.posts_metadata, start=1):
            link = self.url + f'wall.getComments?owner_id={post["owner_id"]}&post_id={post["post_id"]}' \
                              f'&count=100&sort=desc&access_token={VK_TOKEN}&{self.vk_version}'
            response = httpx.get(link).json()
            # Обход ограничение на 5 запросов в секунду
            # if num % 5 == 0:
            #     time.sleep(2)

            for item in response['response']['items']:
                # Добавление данных в бд
                comment_data = {
                    'comment_id': item['id'],
                    'post_id': post['post_id'],
                    'text': item['text']
                }
                if session.query(Comment).filter(Comment.comment_id == comment_data['comment_id']).first() is None:
                    Service.add_comment(comment_data)
                else:
                    Service.update_post(comment_data)

    def main(self):
        self.get_posts()
        # self.get_wall_comments()


if __name__ == '__main__':
    create_tables()
    vk_parser = VkParser()
    vk_parser.main()
