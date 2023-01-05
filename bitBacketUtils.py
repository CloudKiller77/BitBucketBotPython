from atlassian import Bitbucket
import utils
from database import DataBase

PROJECT_NAME = "имя проекта"
REPO_NAME = "имя репозитория"

# Инициализируем класс и вызызваем 2 метода подключение и курсор
database = DataBase()
connection = database.connect_to_db()
cursor = database.create_cursor(connection)

bitbucket_host = utils.HOST_NAME
name = utils.USER_NAME
password = utils.USER_PASSWORD

approves = list()
dictionary = list()
requests = dict()

list_comments = list()
request_comments = dict()
list_comments_id_db = list()

global start_size
global comments


def start_bitbucket():
    bitbucket = Bitbucket(
        url=bitbucket_host,
        username=name,
        password=password,
        verify_ssl=False)
    return bitbucket


def get_all_projects():
    """Получить все проекты"""
    data = start_bitbucket().project_list()
    for project in data:
        print(project)


def get_all_repositories():
    """Получить все репозитории к проекту PROJECT_NAME"""
    data = start_bitbucket().repo_list(PROJECT_NAME)
    for repo in data:
        print(repo["slug"])
        print(repo["project"]["description"])


def get_size_pull_requests() -> int:
    """
    Получить размер массива с реквестами в репозитории

    :return: int() Размер массива с реквестами
    """
    data = list(start_bitbucket().get_pull_requests(PROJECT_NAME, REPO_NAME, limit=10, start=0))
    start_size = len(data)
    return start_size


def get_list_pull_requests() -> list:
    """
    Получить массив с реквестами в репозитории

    :return: list() массив с реквестами
    """
    data = list(start_bitbucket().get_pull_requests(PROJECT_NAME, REPO_NAME, limit=10, start=0))
    return data


def get_dict_with_comments() -> dict:
    # Подготовка словаря для записи в файл
    data = list(start_bitbucket().get_pull_requests(PROJECT_NAME, REPO_NAME, limit=10, start=0))
    library = dict()
    if len(data) > 0:
        for request in data:
            if 'commentCount' not in request['properties']:
                map = {str(request["id"]): str(0)}
                library.update(map)
            else:
                map = {str(request["id"]): str(request['properties']['commentCount'])}
                library.update(map)
    else:
        return library
    return library


def get_open_pull_requests() -> list:
    """
    Получить массив с реквестами из репозитория

    :return: list() Массив с реквестами
    """
    dictionary.clear()
    approves.clear()
    count = 0
    data = list(start_bitbucket().get_pull_requests(PROJECT_NAME, REPO_NAME, limit=10, start=0))
    for request in data:
        approves.clear()
        for user in request["reviewers"]:
            if user["status"] == "APPROVED":
                approves.append(user["status"])
                count = len(approves)
            else:
                continue
        if 'commentCount' not in request['properties']:
            comments = 0
        else:
            comments = request['properties']['commentCount']
        requests = {
            "Commit branch": request["title"],
            "Состояние": request["state"],
            "Имя автора": request["author"]["user"]["displayName"],
            "Роль": request["author"]["role"],
            "Статус проверки": request["author"]["status"],
            "Кол-во проверок": count,
            "Кол-во комментариев": comments,
            "Проверьте меня)": request["links"]["self"][0]["href"]
        }
        dictionary.append(requests)
        count = 0
    # print(dictionary)
    return dictionary


def get_new_comment_request() -> list:
    """
    Получить новый комментраий из реквеста

    :return: list() Массив с комментриями
    """
    ids = list()
    list_comments.clear()

    list_comments_id_db = database.get_list_requests_id(cursor)
    if len(list_comments_id_db) != 0:
        for id in list_comments_id_db:
            var = id[0]
            ids.append(var)
        print(ids)

    data = list(start_bitbucket().get_pull_requests(PROJECT_NAME, REPO_NAME, limit=10, start=0))
    for request in data:
        if 'commentCount' not in request['properties']:
            comments2 = 0
            print("Comments: " + str(comments2))
        elif request["id"] not in ids:
            users = list()
            id = request["id"]
            name = request["author"]["user"]["displayName"].split(" ")
            comm = request['properties']['commentCount']
            users.append(id)
            users.append(name[1])
            users.append(comm)
            print(users)
            # Записывает пользователя с 2-мя комментраиями
            database.safe_new_user_in_db(users, cursor, connection)
        else:
            users = list()
            id = request["id"]
            name = request["author"]["user"]["displayName"].split(" ")
            comm = request['properties']['commentCount']
            comments2 = database.get_comments_form_db(id, cursor)
            if int(comm) > comments2[0]:
                print(comments2)
                users.append(id)
                users.append(name[1])
                users.append(comm)
                request_comments = {
                            "Commit branch": request["title"],
                            "Имя автора": request["author"]["user"]["displayName"],
                            "Кол-во комментариев": comm,
                            "Проверьте меня)": request["links"]["self"][0]["href"]
                        }
                list_comments.append(request_comments)

                database.update_user_comments(id, int(comm), cursor, connection)
            else:
                print(str(comm) + " - " + str(comments2))
    return list_comments


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     get_open_pull_requests()
#     get_new_comment_request()
