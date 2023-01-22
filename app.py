from utils import *
from flask import Flask

CHILDREN_GROUP = ["G"]
FAMILY_GROUP = ["G", "PG", "PG-13"]
ADULT_GROUP = ["R", "NC-17"]

app = Flask(__name__)


app.config['JSON_AS_ASCII'] = False

"""Представление для страницы со списком всех постов"""


@app.route("/movie/<title>")
def film_by_title(title):
    result = get_film_by_title(title)
    return result


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def film_between_year(year_from, year_to):
    result = get_film_between(year_from, year_to)
    return result


@app.route("/rating/children")
def get_for_children():
    result = get_film_by_rating(CHILDREN_GROUP)
    return result


@app.route("/rating/family")
def get_for_family():
    result = get_film_by_rating(FAMILY_GROUP)
    return result


@app.route("/rating/adult")
def get_for_adult():
    result = get_film_by_rating(ADULT_GROUP)
    return result


@app.route("/genre/<genre>")
def get_film_by_genre(genre):
    result = get_last_by_genre(genre)
    return result


if __name__ == "__main__":
    app.run()
