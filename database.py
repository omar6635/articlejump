from sqlobject import *
from random import randint


class SQLMain:
    def __init__(self):
        self.connection = sqlhub.processConnection = connectionForURI("sqlite: word_article_database.db3")
        Word.createTable(ifNotExists=True)
        Article.createTable(ifNotExists=True)

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def insert_word(*args):
        Word(name=args[0], difficulty=args[1], favorite_word=args[2], article_id=args[3])

    @staticmethod
    def create_articles():
        Article(name="Der")
        Article(name="Das")
        Article(name="Die")

    @staticmethod
    def get_random_word():
        query_result = list(Word.select())
        word_to_return_index = randint(0, len(query_result)-1)
        return query_result[word_to_return_index].name, query_result[word_to_return_index].article_id.name


class Word(SQLObject):
    name = StringCol()
    difficulty = IntCol()
    favorite_word = BoolCol()
    article_id = ForeignKey("Article")


class Article(SQLObject):
    name = StringCol()
    word = MultipleJoin("Word")
