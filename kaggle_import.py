import csv
import decimal
import psycopg2
from datetime import date

username = 'postgres'
password = 'DubinaOlga2003'
database = 'k_drama'
host = 'localhost'
port = '5432'
 
INPUT_GENRE = 'import_csv/genres.csv'
INPUT_PEOPLE = 'import_csv/people.csv'
INPUT_SERIES = 'import_csv/series.csv'

query_1 = '''
DELETE FROM genres;
'''
query_2 = '''
DELETE FROM all_series;
'''
query_3 = '''
DELETE FROM genre_series;
'''
query_4 = '''
DELETE FROM cast_series;
'''
query_5 = '''
DELETE FROM rating_date;
'''
query_6 = '''
DELETE FROM people;
'''

query_7 = '''
INSERT INTO genres (id, name_genre) VALUES (%s, %s)
'''
query_8 = '''
select * from genres
'''

query_9 = '''
INSERT INTO people (id, name_actor, birthday, gender) VALUES (%s, %s, %s, %s)
'''
query_10 = '''
select * from people limit 10;
'''

query_11 = '''
INSERT INTO all_series (id, name_series, airing_date) VALUES (%s, %s, %s)
'''
query_12 = '''
select * from all_series limit 10;
'''

query_13 = '''
INSERT INTO rating_date (id, series_id, average_rating, date_rating) VALUES (%s, %s, %s, %s)
'''
query_14 = '''
select * from rating_date limit 10;
'''

query_15 = '''
INSERT INTO genre_series (id, genre_id, series_id) VALUES (%s, %s, %s)
'''
query_16 = '''
select * from genre_series limit 10;
'''

query_17 = '''
INSERT INTO cast_series (id, series_id, actor_id) VALUES (%s, %s, %s)
'''
query_18 = '''
select * from cast_series limit 10;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_3)
    cur.execute(query_4)
    cur.execute(query_5)
    cur.execute(query_2)
    cur.execute(query_6)
    cur.execute(query_1)

    input_file = csv.DictReader(open(INPUT_GENRE))
    for idx, row in enumerate(input_file):
        values = (int(row['tmdb_id']), row['name']) 
        cur.execute(query_7, values)
    cur.execute(query_8)
    for row in cur:
        print(row)

    input_people = csv.DictReader(open(INPUT_PEOPLE, encoding='utf-8'))
    people_id = []
    for idx, row in enumerate(input_people):
        if row['birthday']=='' or row['gender']=='':
            continue
        people_id.append(int(row['tmdb_id']))
        values = (int(row['tmdb_id']), row['name'], row['birthday'], row['gender']) 
        cur.execute(query_9, values)
    cur.execute(query_10)
    for row in cur:
        print(row)

    input_serie = csv.DictReader(open(INPUT_SERIES, encoding='utf-8'))
    count = 1
    count_genre = 1
    count_people = 1
    for idx, row in enumerate(input_serie):
        if row['airing_date']=='' or row['average_rating']=='' or row['genres_ids']=='' or row['cast_ids']=='':
            continue
        #all_series
        values_1 = (int(row['tmdb_id']), row['name'], row['airing_date']) 
        cur.execute(query_11, values_1)
        #rating_date
        values_2 = (count, int(row['tmdb_id']), row['average_rating'], date.today()) 
        cur.execute(query_13, values_2)
        #genre_series
        for genre in row['genres_ids'].split(', '):
            cur.execute(query_15, (count_genre, genre, int(row['tmdb_id'])))
            count_genre +=1
        #cast_series
        amount_people = 0
        for people in row['cast_ids'].split(', '):
            if int(people) not in people_id:
                continue
            cur.execute(query_17, (count_people, int(row['tmdb_id']), people))
            count_people +=1
            amount_people +=1
        count += 1

    cur.execute(query_12)
    for row in cur:
        print(row)
    cur.execute(query_14)
    for row in cur:
        print(row)
    cur.execute(query_16)
    for row in cur:
        print(row)
    cur.execute(query_18)
    for row in cur:
        print(row)
    conn.commit()
