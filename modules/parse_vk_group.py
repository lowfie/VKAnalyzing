from data.config import VK_TOKEN
import httpx
import asyncio

from datetime import datetime

from database.models import Post, Comment, Group
from database import PostService, CommentService, GroupService
from loader import session

from typing import Any

from modules.sentiment_neural_network import SentimentalAnalysisModel


class VkParser:
    def __init__(self) -> None:
        self.url = 'https://api.vk.com/method/'
        self.wall_get = self.url + 'wall.get'
        self.wall_getComments = self.url + 'wall.getComments'
        self.groups_getGroup = self.url + 'groups.getById'
        self.groups_getMembers = self.url + 'groups.getMembers'
        self.vk_version = 5.131
        self.posts_metadata: list[dict[str, Any]] = []
        self.group_metadata: list[dict[str, Any]] = []
        self.sentiment_model = SentimentalAnalysisModel()

    async def get_group_byid(self, group: str) -> None:
        """
        Функция принимает на вход имя в ссылке группы и собирает данные
        Далее она сохраняет в бд и передаёт параметры для сбора постов
        И комментариев
        """
        params = {
            'group_id': group,
            'access_token': VK_TOKEN,
            'count': 0,
            'v': self.vk_version
        }
        get_group = httpx.get(self.groups_getGroup, params=params).json()['response'][0]
        get_group_members = httpx.get(self.groups_getMembers, params=params).json()['response']

        group_data = {
            'group_id': get_group['id'],
            'name': get_group['name'],
            'screen_name': get_group['screen_name'],
            'members': get_group_members['count']
        }
        # Инициализация класса для сохранения в бд
        service_group = GroupService(Group)

        # Формирование списка с данным для сбора постов
        self.group_metadata.append(group_data)

        # Сохранение и обновление данных в бд
        if session.query(Group).filter(Group.group_id == group_data['group_id']).first() is None:
            service_group.add(group_data)
        else:
            service_group.update(group_data)

    async def get_posts(self) -> None:
        """
        Парсинг данных последних постов из группы вк
        И занесение данных в бд
        """
        for group in self.group_metadata:
            params = {
                'domain': group['screen_name'],
                'count': 60,
                'access_token': VK_TOKEN,
                'v': self.vk_version
            }
            response = httpx.get(self.wall_get, params=params).json()

            # Инициализация класса для сохранения в бд
            service_post = PostService(Post)

            # Список из 40 последних постов
            items = [item for item in response['response']['items']]

            for item in items:
                self.posts_metadata.append({'post_id': item['id'], 'owner_id': item['owner_id']})
                # Добавление данных в таблицу posts
                post_data = {
                    'post_id': item['id'],
                    'owner_id': item['owner_id'],
                    'group_id': group['group_id'],
                    'likes': item['likes']['count'],
                    'quantity_comments': item['comments']['count'],
                    'reposts': item['reposts']['count'],
                    'views': item['views']['count'],
                    'photo': True if 'attachments' in item else False,
                    'text': item['text'],
                    'date': datetime.fromtimestamp(item['date'])
                }
                if session.query(Post).filter(Post.post_id == post_data['post_id']).first() is None:
                    service_post.add(post_data)
                else:
                    service_post.update(post_data)

    async def get_wall_comments(self) -> None:
        """
        Парсинг комментариев поста
        И занесение данных в бд
        """

        # Инициализация класса для сохранения в бд
        service_comment = CommentService(Comment)
        service_post = PostService(Post)

        # Перебор всех постов для получения комментариев
        for num, post in enumerate(self.posts_metadata, start=1):
            params = {
                'owner_id': post['owner_id'],
                'post_id': post['post_id'],
                'count': 100,
                'sort': 'desc',
                'access_token': VK_TOKEN,
                'v': self.vk_version
            }
            response = httpx.get(self.wall_getComments, params=params).json()
            # Обход ограничение на 5 запросов в секунду
            if num % 4 == 0:
                await asyncio.sleep(2)

            # Итерация всех комментариев поста
            for item in response.get('response').get('items'):
                if len(item['text'].split()) > 1:
                    # Добавление данных в бд
                    tone = self.sentiment_model.set_tone_of_the_comment([item['text']])
                    comment_data = {
                        'comment_id': item['id'],
                        'post_id': post['post_id'],
                        'text': item['text'],
                        'tone': tone
                    }
                    if session.query(Comment).filter(Comment.comment_id == comment_data['comment_id']).first() is None:
                        service_comment.add(comment_data)
                        service_post.update_tonal_comments(tone, post['post_id'])
                    else:
                        service_comment.update(comment_data)

    async def run_vk_parser(self, group: str) -> None:
        tasks = [
            self.get_group_byid(group),
            self.get_posts(),
            self.get_wall_comments()
        ]

        await asyncio.gather(*tasks)
