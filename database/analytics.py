from sqlalchemy.orm.attributes import InstrumentedAttribute
from loader import session, Base
from sqlalchemy import func

from database.services import GroupService

from datetime import datetime, timedelta
from typing import Any


class Analytics:
    """
    Класс в котором проходят все статистические расчёты
    И на их основе аналитика
    """

    def __init__(self, group: Base, post: Base) -> None:
        self.group = group
        self.post = post

    def get_statistic(self, input_data: dict[str, str]) -> dict[str, Any] | None:
        """
        Функция принимает словарь со значениями
        периода времени и группы
        Далее функция возвращает словарь со статистикой
        """
        service_group = GroupService(self.group)
        group_id = service_group.get_group_id(input_data["name"])
        if input_data["choice"] == "choicePeriod":
            from_date = datetime.now()
            to_date = datetime.strptime(input_data["date"], "%Y-%m-%d %H:%M:%S")
            days = (from_date - to_date).days
        else:
            from_date = datetime.strptime(input_data["date"], "%Y-%m-%d %H:%M:%S") + timedelta(hours=24)
            to_date = datetime.strptime(input_data["date"], "%Y-%m-%d %H:%M:%S")
            days = (from_date - to_date).days

        if group_id:
            # Количество подписчиков группы
            group_name, group_members = (
                session.query(self.group.group_name, self.group.group_members)
                .filter(
                    self.group.group_id == group_id
                )
                .first()
            )

            # Количество постов за период
            count_post = (
                session.query(func.count(self.post.post_id))
                .filter(
                    self.post.group_id == group_id,
                    self.post.date.between(to_date, from_date)
                )
                .first()[0]
            )

            # Количество постов с фото/видео за период
            count_post_with_photo = (
                session.query(func.count(self.post.post_id))
                .filter(
                    self.post.group_id == group_id,
                    self.post.date.between(to_date, from_date),
                    self.post.photo == "true",
                )
                .first()[0]
            )

            def get_sum_record(query_param: InstrumentedAttribute) -> int:
                parameter = (
                    session.query(func.sum(query_param))
                    .filter(
                        self.post.group_id == group_id,
                        self.post.date.between(to_date, from_date)
                    )
                    .first()[0]
                )
                return parameter

            likes = get_sum_record(self.post.likes)
            views = get_sum_record(self.post.views)
            comments = get_sum_record(self.post.quantity_comments)
            reposts = get_sum_record(self.post.reposts)

            reactions = likes + comments + reposts
            engagement_rate = float("{0:.2f}".format((reactions / (days * group_members)) * 100))
            count_user_er = int(engagement_rate / 100 * group_members)

            statistic = {
                "group_name": group_name,
                "group_members": group_members,
                "count_post": count_post,
                "posts_with_photo": count_post_with_photo,
                "likes": likes,
                "views": views,
                "comments": comments,
                "reposts": reposts,
                "engagement_rate": engagement_rate,
                "er_users": count_user_er,
                "to_date": to_date,
                "from_date": from_date
            }
            return statistic
        return None

    def get_top_stats(self, input_data: dict[str, str], query_param: InstrumentedAttribute) -> list[dict[str, Any]]:
        """
        Функция принимает словарь со значением и параметром.
        Ведёт подсчёт максимального параметра и на основе этого
        возвращает ссылку на пост
        """
        service_group = GroupService(self.group)
        group_id = service_group.get_group_id(input_data["name"])
        top_stats_url_list = []

        if group_id:
            max_values_record = (
                session.query(query_param)
                .distinct()
                .filter(
                    self.post.group_id == group_id, self.post.date >= input_data["date"]
                )
                .order_by(query_param.desc())
                .limit(3)
                .all()
            )
            for num, max_value_record in enumerate(max_values_record, start=1):
                owner_id = (
                    session.query(self.post.owner_id)
                    .filter(
                        self.post.group_id == group_id,
                        self.post.date >= input_data["date"],
                        query_param == max_value_record[0]
                    )
                    .first()[0]
                )
                post_id = (
                    session.query(self.post.post_id)
                    .filter(
                        self.post.owner_id == owner_id, query_param == max_value_record[0]
                    )
                    .first()[0]
                )

                to_date = (
                    session.query(self.post.date)
                    .filter(
                        self.post.group_id == group_id,
                        self.post.date >= input_data["date"],
                    )
                    .first()[0]
                )

                # Название ссылки
                if num == 1:
                    text = "🥇 Первое место"
                elif num == 2:
                    text = "🥈 Второе место"
                else:
                    text = "🥉 Третье место"

                top_stat_url = {
                    "number": f"{text}",
                    "url": f"https://vk.com/{input_data['name']}?w=wall{owner_id}_{post_id}",
                    "to_date": to_date
                }
                top_stats_url_list.append(top_stat_url)
        return top_stats_url_list
