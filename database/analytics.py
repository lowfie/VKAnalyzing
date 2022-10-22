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
        date_params = self.get_date_params(input_data["choice"], input_data["date"], group_id)

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
                    self.post.date.between(date_params["from_date"], date_params["to_date"])
                )
                .first()[0]
            )

            # Количество постов с фото/видео за период
            count_post_with_photo = (
                session.query(func.count(self.post.post_id))
                .filter(
                    self.post.group_id == group_id,
                    self.post.date.between(date_params["from_date"], date_params["to_date"]),
                    self.post.photo == "true",
                )
                .first()[0]
            )

            def get_sum_record(query_param: InstrumentedAttribute) -> int:
                parameter = (
                    session.query(func.sum(query_param))
                    .filter(
                        self.post.group_id == group_id,
                        self.post.date.between(date_params["from_date"], date_params["to_date"])
                    )
                    .first()[0]
                )
                return parameter

            likes = get_sum_record(self.post.likes)
            views = get_sum_record(self.post.views)
            comments = get_sum_record(self.post.quantity_comments)
            reposts = get_sum_record(self.post.reposts)

            reactions = likes + comments + reposts
            engagement_rate = float("{0:.2f}".format((reactions / (date_params["days"] * group_members)) * 100))
            count_user_er = int(engagement_rate / 100 * group_members)

            statistics = {
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
                "to_date": str(date_params["to_date"].replace(second=0, microsecond=0))[:date_params["line_slice"]],
                "from_date": str(date_params["from_date"].replace(second=0, microsecond=0))[:date_params["line_slice"]],
                "date_last_post": date_params["date_last_post"]
            }
            if input_data["choice"] == "choicePeriod":
                statistics["to_date"] = statistics["date_last_post"]
            return statistics
        return None

    def get_top_stats(self, input_data: dict[str, str], query_param: InstrumentedAttribute) -> None | list[dict[str, Any]]:
        """
        Функция принимает словарь со значением и параметром.
        Ведёт подсчёт максимального параметра и на основе этого
        возвращает ссылку на пост
        """
        service_group = GroupService(self.group)
        group_id = service_group.get_group_id(input_data["name"])
        top_stats_url_list = []
        date_params = self.get_date_params(input_data["choice"], input_data["date"], group_id)

        if group_id:
            max_values_record = (
                session.query(query_param)
                .distinct()
                .filter(
                    self.post.group_id == group_id,
                    self.post.date.between(date_params["from_date"], date_params["to_date"])
                )
                .order_by(query_param.desc())
                .limit(3)
                .all()
            )
            if not max_values_record:
                return None

            for num, max_value_record in enumerate(max_values_record, start=1):
                owner_id = (
                    session.query(self.post.owner_id)
                    .filter(
                        self.post.group_id == group_id,
                        self.post.date.between(date_params["from_date"], date_params["to_date"]),
                        query_param == max_value_record[0]
                    )
                    .first()[0]
                )
                post_id = (
                    session.query(self.post.post_id)
                    .filter(
                        self.post.owner_id == owner_id,
                        query_param == max_value_record[0]
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
                    "to_date": str(date_params["to_date"]
                                   .replace(second=0, microsecond=0))[:date_params["line_slice"]],
                    "from_date": str(date_params["from_date"]
                                     .replace(second=0, microsecond=0))[:date_params["line_slice"]],
                    "date_last_post": date_params["date_last_post"]
                }
                if input_data["choice"] == "choicePeriod":
                    top_stat_url["to_date"] = top_stat_url["date_last_post"]

                top_stats_url_list.append(top_stat_url)
        return top_stats_url_list

    def get_date_params(self, choice: str, date: str, group_id: int) -> dict[str, Any]:
        to_date_period = (
            session.query(self.post.date)
            .filter(
                self.post.group_id == group_id,
                self.post.date >= date,
            )
            .first()[0]
        )
        if choice == "choicePeriod":
            to_date_last_post = to_date_period
            to_date = datetime.now().replace(microsecond=0)
            from_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            days = (to_date - from_date).days
            line_slice = -3
        else:
            to_date_last_post = to_date_period
            to_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=24)
            from_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            days = (to_date - from_date).days
            line_slice = -8
        return {"to_date": to_date, "from_date": from_date, "days": days, "line_slice": line_slice,
                "date_last_post": to_date_last_post}
