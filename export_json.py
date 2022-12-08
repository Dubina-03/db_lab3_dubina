import json
import psycopg2

username = 'postgres'
password = 'DubinaOlga2003'
database = 'k_drama'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:

    cur = conn.cursor()
    
    for table in ('all_series', 'cast_series', 'genre_series', 'genres', 'people', 'rating_date'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('export_csv_json/all_data.json', 'w') as outf:
    json.dump(data, outf, default = str)
    