import csv
import sqlite3

from django.core.management.base import BaseCommand


FILES_CSV = {
    'category.csv': 'reviews_category', 'genre.csv': 'reviews_genre',
    'titles.csv': 'reviews_title', 'users.csv': 'reviews_user',
    'genre_title.csv': 'reviews_genretitle', 'review.csv': 'reviews_review',
    'comments.csv': 'reviews_comment'
}


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        for name_file, name_table in FILES_CSV.items():
            with open(f'static/data/{name_file}',
                      'r', encoding='UTF-8') as file:
                contents = csv.reader(file)
                next(file, None)
                col_names, number_questions = self.get_col_names(cursor,
                                                                 name_table)
                insert_records = (f'INSERT INTO {name_table} ({col_names})'
                                  f'VALUES({number_questions})')
                cursor.executemany(insert_records, contents)

        connection.commit()
        connection.close()

    def get_col_names(self, cursor, tablename):
        reader = cursor.execute(f"SELECT * FROM {tablename}")
        col_names = ', '.join([x[0] for x in reader.description])
        number_questions = ', '.join(['?' for x in
                                      range(len(reader.description))])
        return col_names, number_questions
