from loader import session
from sqlalchemy import func


class GroupService:

    def __init__(self, group):
        self.group = group

    def add(self, input_data: dict):
        new_group = self.group(
            group_id=input_data['group_id'],
            group_name=input_data['name'],
            screen_name=input_data['screen_name'],
            group_members=input_data['members']
        )
        session.add(new_group)
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при сохранении Поста, Текст ошибки:', err)
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        group = session.query(self.group).filter(self.group.group_id == input_data['group_id']).first()
        if not group:
            raise ValueError('Такого поста нет в бд')
        group.group_name = input_data['name']
        group.screen_name = input_data['screen_name']
        group.group_members = input_data['members']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Поста, Текст ошибки:', err)
            session.rollback()


class PostService:

    def __init__(self, post):
        self.post = post

    def add(self, input_data: dict):
        """
        Функция принимает словарь с данными поста
        и добавляет эти данные бд, если их не существует
        """
        new_post = self.post(
            post_id=input_data['post_id'],
            owner_id=input_data['owner_id'],
            group_id=input_data['group_id'],
            quantity_comments=input_data['quantity_comments'],
            reposts=input_data['reposts'],
            likes=input_data['likes'],
            views=input_data['views'],
            photo=input_data['photo'],
            post_text=input_data['text'],
            date=input_data['date']
        )
        session.add(new_post)
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при сохранении Поста, Текст ошибки:', err)
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        post = session.query(self.post).filter(self.post.post_id == input_data['post_id']).first()
        if not post:
            raise ValueError('Такого поста нет в бд')
        post.quantity_comments = input_data['quantity_comments']
        post.likes = input_data['likes']
        post.views = input_data['views']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Поста, Текст ошибки:', err)
            session.rollback()

    def get_statistic(self, input_data: dict):
        """
        Функция принимает словарь со значениями
        периода времени и группы
        Далее функция возвращает словарь со статистикой
        """

        if session.query(self.post).filter(self.post.group == input_data['name']).first():
            # Количество постов за период
            posts = session.query(func.count(self.post.post_id)).filter(
                self.post.group == input_data['name'],
                self.post.date >= input_data['date']
            ).first()[0]

            # Количество постов с фото/видео за период
            post_with_photo = session.query(func.count(self.post.post_id)).filter(
                self.post.group == input_data['name'],
                self.post.date >= input_data['date'],
                self.post.photo == 'true'
            ).first()[0]

            def get_sum_record(data, query_param):
                parameter = session.query(func.sum(query_param)).filter(
                    self.post.group == data['name'],
                    self.post.date >= data['date'],
                ).first()[0]
                return parameter

            def get_most_value_record(data, query_param):
                max_value_record = session.query(func.max(query_param)).filter(
                    self.post.group == data['name'],
                    self.post.date >= data['date']
                ).first()[0]
                owner_id = session.query(self.post.owner_id).filter(
                    self.post.group == data['name'],
                    self.post.date >= data['date'],
                    query_param == max_value_record
                ).first()[0]
                post_id = session.query(self.post.post_id).filter(
                    self.post.owner_id == owner_id,
                    query_param == max_value_record
                ).first()[0]
                return {'owner_id': owner_id, 'post_id': post_id}

            def get_url_most_value_record(data, query_param):
                params = get_most_value_record(data, query_param)
                owner_id = params['owner_id']
                post_id = params['post_id']
                return f'https://vk.com/{data["name"]}?w=wall{owner_id}_{post_id}'

            statistic = {
                'count_post': posts,
                'posts_with_photo': post_with_photo,
                'likes': get_sum_record(input_data, self.post.likes),
                'views': get_sum_record(input_data, self.post.views),
                'comments': get_sum_record(input_data, self.post.quantity_comments),
                'reposts': get_sum_record(input_data, self.post.reposts),
                'negative_post': get_url_most_value_record(input_data, self.post.negative_comments),
                'positive_post': get_url_most_value_record(input_data, self.post.positive_comments),
                'popular_post': get_url_most_value_record(input_data, self.post.views)
            }
            return statistic
        else:
            return False

    def update_tonal_comments(self, tone, where_post):
        if tone == 'positive':
            column = {'positive_comments': (self.post.positive_comments + 1)}
        elif tone == 'negative':
            column = {'negative_comments': (self.post.negative_comments + 1)}
        else:
            column = {'negative_comments': self.post.negative_comments}

        session.query(self.post).filter(self.post.post_id == where_post).update(column)

        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Поста, Текст ошибки:', err)
            session.rollback()


class CommentService:

    def __init__(self, comment):
        self.comment = comment

    def add(self, input_data: dict):
        """
        Функция принимает словарь метаданных комментария
        И добавляет в бд
        """
        new_comment = self.comment(
            comment_id=input_data['comment_id'],
            post_id=input_data['post_id'],
            text=input_data['text'],
            tone=input_data['tone']
        )
        session.add(new_comment)
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при сохранении Комментария, Текст ошибки:', err)
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает на вход метаданные комментария
        и обновляет их
        """
        comment = session.query(self.comment).filter(self.comment.comment_id == input_data['comment_id']).first()
        if not comment:
            raise ValueError('Такого комментария нет в бд')
        comment.text = input_data['text']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Комментария, Текст ошибки:', err)
            session.rollback()
