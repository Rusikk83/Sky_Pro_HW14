import sqlite3
import json


def list_to_str_query(list_of_value: list):
    """Преабразует набор параметров в строку со значениями в апострофах через запятую"""
    result = ""
    for el in list_of_value:
        result += f"'{el}', "
    return result[:-2]


def get_film_by_title(title):
    """ШАГ 1. Реализует поиск фильмов по названию"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = f"""
            select 
            title,
            country,
            release_year,
            listed_in as genre,
            description
            from netflix
            where title = '{title}'
            order by date_added DESC
            """
        response = cursor.execute(query)
        result = response.fetchone()

    res = dict()
    for key in result.keys():
        res[key] = result[key]

    return res


def get_film_between(year_from, year_to):
    """ШАГ 2. Выполняет поиск по диапазону лет"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = f"""
            select 
            title,
            release_year
            from netflix
            where release_year between {year_from} and {year_to}
            limit 100"""
        response = cursor.execute(query)
        result = response.fetchall()
    film_list = []
    for item in result:
        res = dict()
        for key in item.keys():
            res[key] = item[key]
        film_list.append(res)

    return film_list


def get_film_by_rating(rating_list):
    """ШАГ 3. Выполняет поиск по набору рейтингов"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = f"""
            select 
            title,
            rating,
            description
            from netflix
            where rating IN ({list_to_str_query(rating_list)})
            limit 100"""
        response = cursor.execute(query)
        result = response.fetchall()
    film_list = []
    for item in result:
        res = dict()
        for key in item.keys():
            res[key] = item[key]
        film_list.append(res)

    return film_list


def get_last_by_genre(genre):
    """ШАГ 4. Возвращает 10 самых свежих фильмов по жанру"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = f"""
            select 
            title,
            description
            from netflix
            where listed_in LIKE '%{genre}%'
            order by date_added desc
            limit 10"""
        response = cursor.execute(query)
        result = response.fetchall()
    film_list = []
    for item in result:
        res = dict()
        for key in item.keys():
            res[key] = item[key]
        film_list.append(res)

    return json.dumps(film_list)


def get_cast(cast1, cast2):
    """ШАГ 5. Возвращает список актеров снимавшихся более двух раз одновременно в паре с заданными"""
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""
            select [cast] as actor
            from netflix 
            where actor LIKE '%{cast1}%'
            and actor LIKE '%{cast2}%'
            """
        response = cursor.execute(query)
        result = response.fetchall()
    casts_film = set()
    list_cast_find = []
    list_cast_more_two = []
    casts_for_find = {cast1, cast2}
    for item in result:
        casts_film = set(item[0].split(', ')).difference(casts_for_find)
        list_cast_find += list(casts_film)

    for item in list_cast_find:
        if item not in list_cast_more_two and list_cast_find.count(item) > 2:
            list_cast_more_two.append(item)

    return list_cast_more_two


def get_film_by_scope(film_type, year, genre):
    """ШАГ 6. Выполняет поиск по типу, жанру и году"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = f"""
            select 
            title,
            description
            from netflix
            where listed_in LIKE '%{genre}%'
            AND release_year = {year}
            AND type = '{film_type}'
            limit 10"""
        response = cursor.execute(query)
        result = response.fetchall()
    film_list = []
    for item in result:
        res = dict()
        for key in item.keys():
            res[key] = item[key]
        film_list.append(res)

    return json.dumps(film_list)


"""проверка функций для которых нет представления"""
print(get_cast("Jack Black", "Dustin Hoffman"))
print(get_film_by_scope('Movie', 2016, 'Dramas'))
