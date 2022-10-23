import httpx
import asyncio

from typing import Any
from loguru import logger
from loader import session
from datetime import datetime
from data.config import VK_TOKEN

from database.models import Post, Comment, Group
from database import PostService, CommentService, GroupService

from modules.sentiment_neural_network import SentimentalAnalysisModel


class VkParser:
    def __init__(self) -> None:
        # Объекты для VK_API
        self.url = "https://api.vk.com/method/"
        self.wall_get = self.url + "wall.get"
        self.wall_getComments = self.url + "wall.getComments"
        self.groups_getGroup = self.url + "groups.getById"
        self.groups_getMembers = self.url + "groups.getMembers"
        self.vk_version = 5.131

        # Объекты для базы данных
        self.group_metadata: list[dict[str, Any]] = []
        self.group_update_metadata: list[dict[str, Any]] = []
        self.posts_metadata: list[dict[str, Any]] = []
        self.posts_update_metadata: list[dict[str, Any]] = []
        self.comments_metadata: list[dict[str, Any]] = []
        self.comments_update_metadata: list[dict[str, Any]] = []

        # Инициализация модели нейросети для анализа тональности текста
        self.sentiment_model = SentimentalAnalysisModel()

    async def get_group_byid(self, group: str) -> bool:
        """
        Функция принимает на вход имя в ссылке группы и собирает данные
        Далее она сохраняет в бд и передаёт параметры для сбора постов
        И комментариев
        """
        logger.info(f"Начался сбор групп")

        params_get_group = {
            "group_id": group,
            "access_token": VK_TOKEN,
            "count": 0,
            "v": self.vk_version,
        }
        try:
            get_group = httpx.get(self.groups_getGroup, params=params_get_group).json()["response"][0]
        except KeyError:
            logger.warning('Ошибка парсинга группы (Ошибка get-запроса: невозможно собрать данные)')
            return False

        params_group_members = {
            "group_id": get_group["id"],
            "access_token": VK_TOKEN,
            "count": 0,
            "v": self.vk_version,
        }
        get_group_members = httpx.get(
            self.groups_getMembers, params=params_group_members
        ).json()["response"]

        group_data = {
            "group_id": get_group["id"],
            "group_name": get_group["name"],
            "screen_name": get_group["screen_name"],
            "group_members": get_group_members["count"],
        }

        # Инициализация класса для сохранения в бд
        service_group = GroupService(Group)

        # Сохранение и обновление данных групп в бд
        if (
            session.query(Group)
            .filter(Group.group_id == group_data["group_id"])
            .first()
            is None
        ):
            # Формирование списка с данным для сбора постов
            self.group_metadata.append(group_data)
            service_group.add_all(self.group_metadata)
        else:
            # Формирование списка с данным для обновления постов
            self.group_update_metadata.append(group_data)
            service_group.update_all(self.group_metadata)
        return True

    async def get_posts(self) -> None:
        """
        Парсинг данных последних постов из группы вк
        И занесение данных в бд
        """
        logger.info(f"Начался сбор постов")

        # Инициализация класса для сохранения в бд
        service_post = PostService(Post)
        all_groups = self.group_metadata + self.group_update_metadata
        for group in all_groups:
            params = {
                "domain": group["screen_name"],
                "count": 60,
                "access_token": VK_TOKEN,
                "v": self.vk_version,
            }
            response = httpx.get(self.wall_get, params=params).json()

            # Список из 60 последних постов
            for post in response["response"]["items"]:
                # Добавление данных в таблицу posts
                post_data = {
                    "post_id": post["id"],
                    "owner_id": post["owner_id"],
                    "group_id": group["group_id"],
                    "likes": post["likes"]["count"],
                    "quantity_comments": post["comments"]["count"],
                    "reposts": post["reposts"]["count"],
                    "views": post["views"]["count"],
                    "photo": True if "attachments" in post else False,
                    "post_text": post["text"],
                    "date": datetime.fromtimestamp(post["date"]),
                }
                if (
                    session.query(Post)
                    .filter(Post.post_id == post_data["post_id"])
                    .first()
                    is None
                ):
                    self.posts_metadata.append(post_data)
                else:
                    self.posts_update_metadata.append(post_data)

        # Сохранение данных постов в бд
        service_post.add_all(self.posts_metadata)
        service_post.update_all(self.posts_update_metadata)

    async def get_wall_comments(self) -> None:
        """
        Парсинг комментариев поста
        И занесение данных в бд
        """
        logger.info(f"Начался сбор комментариев")

        # Инициализация класса для сохранения в бд
        service_comment = CommentService(Comment)
        service_post = PostService(Post)

        # Перебор всех постов для получения комментариев
        all_posts = self.posts_metadata + self.posts_update_metadata
        for num, post in enumerate(all_posts, start=1):
            params = {
                "owner_id": post["owner_id"],
                "post_id": post["post_id"],
                "count": 100,
                "sort": "desc",
                "access_token": VK_TOKEN,
                "v": self.vk_version,
            }
            response = httpx.get(self.wall_getComments, params=params).json()

            # Обход ограничение на 5 запросов в секунду
            if num % 4 == 0:
                await asyncio.sleep(2)

            # Список количества позитивных/негативных комментариев у поста
            tones_post = {
                "post_id": post["post_id"],
                "positive_comments": 0,
                "negative_comments": 0,
            }

            # Итерация всех комментариев поста
            for comment in response["response"]["items"]:
                if len(comment["text"].split()) > 1:
                    # Добавление данных в бд
                    tone = self.sentiment_model.set_tone_comment([comment["text"]])
                    comment_data = {
                        "comment_id": comment["id"],
                        "post_id": post["post_id"],
                        "text": comment["text"],
                        "tone": tone,
                    }
                    if (
                        session.query(Comment)
                        .filter(Comment.comment_id == comment_data["comment_id"])
                        .first()
                        is None
                    ):
                        self.comments_metadata.append(comment_data)
                        # подсчёт позитивных/негативных комментариев поста
                        if tone == "positive":
                            tones_post["positive_comments"] += 1
                        elif tone == "negative":
                            tones_post["negative_comments"] += 1
                    else:
                        self.comments_update_metadata.append(comment_data)

            # Обновление количества позитивных/негативных комментариев поста
            service_post.update_tonal_comments(tones_post)

        service_comment.add_all(self.comments_metadata)
        service_comment.update_all(self.comments_update_metadata)

    async def run_vk_parser(self, group: str) -> None | bool:
        tasks = [self.get_group_byid(group), self.get_posts(), self.get_wall_comments()]
        result_tasks = await asyncio.gather(*tasks)
        if False in result_tasks:
            return False
        else:
            return True
