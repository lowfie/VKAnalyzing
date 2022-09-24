from data.config import VK_TOKEN
import httpx
import asyncio

from datetime import datetime

from database.models import Post, Comment
from database import PostService, CommentService
from loader import session


class VkParser:
    def __init__(self):
        self.url = 'https://api.vk.com/method/'
        self.vk_version = 'v=5.131'
        self.posts_metadata = []

    async def get_posts(self, group):
        """
        Парсинг данных 40 последних постов из группы вк
        И занесение данных в бд
        """
        link = self.url + f'wall.get?domain={group}&count=40&access_token={VK_TOKEN}&{self.vk_version}'
        response = httpx.get(link).json()

        service_post = PostService(Post)

        # Список из 40 последних постов
        items = [item for item in response['response']['items']]

        for item in items:
            self.posts_metadata.append({'post_id': item['id'], 'owner_id': item['owner_id']})
            # Добавление данных в бд
            # Попробовать добавить bulk_insert_mappings (Оптимизация)
            post_data = {
                'id': item['id'],
                'owner_id': item['owner_id'],
                'group': group,
                'quantity_comments': item['comments']['count'],
                'likes': item['likes']['count'],
                'views': item['views']['count'],
                'photo': True if 'attachments' in item else False,
                'text': item['text'],
                'date': datetime.fromtimestamp(item['date'])
            }
            if session.query(Post).filter(Post.post_id == post_data['id']).first() is None:
                service_post.add(post_data)
            else:
                service_post.update(post_data)

    async def get_wall_comments(self):
        """
        Парсинг комментариев поста
        И занесение данных в бд
        """
        service_comment = CommentService(Comment)
        for num, post in enumerate(self.posts_metadata, start=1):
            link = self.url + f'wall.getComments?owner_id={post["owner_id"]}&post_id={post["post_id"]}' \
                              f'&count=100&sort=desc&access_token={VK_TOKEN}&{self.vk_version}'
            response = httpx.get(link).json()
            # Обход ограничение на 5 запросов в секунду
            if num % 4 == 0:
                await asyncio.sleep(2)

            for item in response.get('response').get('items'):
                if item:
                    if len(item['text'].split()) > 1:
                        # Добавление данных в бд
                        comment_data = {
                            'comment_id': item['id'],
                            'post_id': post['post_id'],
                            'text': item['text']
                        }
                        if session.query(Comment).filter(Comment.comment_id == comment_data['comment_id']).first() is None:
                            service_comment.add(comment_data)
                        else:
                            service_comment.update(comment_data)

    async def run_vk_parser(self, group):
        tasks = [
            self.get_posts(group),
            self.get_wall_comments()
        ]

        await asyncio.gather(*tasks)
