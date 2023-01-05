import sqlite3 as sq


class DataBase:
    comment = int()
    requests_id = list()

    def connect_to_db(self) -> sq.Connection:
        """
        Подключение к базе "bitbucket.db", если ее нет она будет создана

        :return: connection Соединение с базой
        """
        with sq.connect("bitbucket.db") as connection:
            return connection

    def create_cursor(self, connection) -> sq.Cursor:
        """
        Создает и возвращает курсор для работы с базой

        :param connection: Соединение с базой
        :return: cursor Курсор
        """
        cursor = connection.cursor()
        return cursor

    def close_db(self, connection):
        """
        Закрывает соединение с базой

        :param connection: Соединение с базой
        :return: Закрывает соединение с базой
        """
        connection.close()

    def create_table(self, connection, cursor):
        """
        Создает таблицу, куда будут писаться:
        userId: id реквеста
        userName: имя пользователя
        countCm: кол-во комментариев к реквесту

        :param connection: Соединение с базой
        :param cursor: Курсор для работы с базой
        :return: Создает таблицу
        """
        cursor.execute("""CREATE TABLE IF NOT EXISTS comments(
        userId INTEGER DEFAULT 0,
        userName TEXT NOT NULL,
        countCm INTEGER DEFAULT 0)""")
        connection.commit()

    def get_comments_form_db(self, user_id, cursor) -> int:
        """
        Получить кол-во комментариев по user_id реквеста

        :param user_id: id реквеста
        :param cursor: Курсор для работы с базой
        :return: int() Кол-во комментариев в реквесте
        """
        global comment
        cursor.execute(f"SELECT countCm FROM comments WHERE userId={user_id}")
        comment = cursor.fetchone()
        return comment

    def get_list_requests_id(self, cursor) -> list:
        """
        Возвращает все id реквесты которые есть в базе

        :param cursor: Курсор для работы с базой
        :return: list() Получает все id реквестов в базе
        """
        global requests_id
        cursor.execute("SELECT userId FROM comments")
        requests_id = cursor.fetchall()
        return requests_id

    def safe_new_user_in_db(self, users, cursor, connection):
        """
        Записывает в базу инфо по новому пользователю, создавшему реквест

        :param users: list() Инфо по пользователю
        :param cursor: Курсор для работы с базой
        :param connection: Соединение с базой
        :return: Создает запись нового пользователя
        """
        cursor.execute("INSERT INTO comments VALUES(?, ?, ?);", users)
        connection.commit()

    def update_user_comments(self, user_id, comm, cursor, connection):
        """
        Обновляет запись в базе по id реквеста, переписывает кол-во комментариев

        :param user_id: int() id реквеста
        :param comm: int() Кол-во комментариев
        :param cursor: Курсор для работы с базой
        :param connection: Соединение с базой
        :return: Переписывает кол-во комментариев по id реквеста
        """
        cursor.execute(f"UPDATE comments SET countCm={comm} WHERE userId={user_id}")
        connection.commit()

    def delete_user_from_db(self, name, cursor, connection):
        """
        Удаляет пользователя с базы по его Имени

        :param name: str() Имя пользователя
        :param cursor: Курсор для работы с базой
        :param connection: Соединение с базой
        :return: Удаляет пользователя
        """
        cursor.execute(f"DELETE FROM comments WHERE userName='{name}'")
        connection.commit()

    def delete_table(self, table_name, cursor):
        """
        Удаляет таблицу по названию table_name

        :param table_name: Название таблицы
        :param cursor: Курсор для работы с базой
        :return: Удаляет таблицу
        """
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# if __name__ == '__main__':
#     create_table(connect_to_db(), create_cursor(connect_to_db()))
#     # delete_table("comments", create_cursor(connect_to_db()))
#     close_db(connect_to_db())
