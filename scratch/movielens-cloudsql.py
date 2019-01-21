import csv
import sys

import mysql.connector

from datetime import datetime


def create_tables(db):
    movies_table_sql = """
    CREATE TABLE IF NOT EXISTS movies (
        movieid integer PRIMARY KEY,
        title varchar(255) NOT NULL,
        year integer NOT NULL,
        tmdb varchar(20),
        imdb varchar(20),
        poster varchar(255)
    )
    """

    ratings_table_sql = """
    CREATE TABLE IF NOT EXISTS ratings (
        ratingid integer PRIMARY KEY AUTO_INCREMENT,
        movieid integer NOT NULL,
        userid integer NOT NULL,
        rating float NOT NULL,
        ts datetime NOT NULL
    )
    """

    genres_table_sql = """
    CREATE TABLE IF NOT EXISTS genres (
        genreid integer PRIMARY KEY,
        name varchar(255) NOT NULL,
        count integer NOT NULL
    )
    """

    genres_movies_table_sql = """
    CREATE TABLE IF NOT EXISTS genres_movies (
        genreid integer NOT NULL,
        movieid integer NOT NULL
    )
    """

    cursor = db.cursor()
    cursor.execute(movies_table_sql)
    cursor.execute(ratings_table_sql)
    cursor.execute(genres_table_sql)
    cursor.execute(genres_movies_table_sql)
    db.commit()
    cursor.close()


def parse_movies(db, mfile):
    # movies = []
    mcsv = csv.DictReader(mfile)

    genre_movies = {}
    # insert_sql = "INSERT INTO movies (movieid, title, year) VALUES (%s, %s, %s)"

    for row in mcsv:
        movieid = int(row['movieId'])
        # title = row['title'].split(' (')[0]
        # year = row['title'].split(' (')[-1][:-1]
        genres = row['genres'].split('|')

        # movies.append(
        #     (movieid, title, year)
        # )

        for g in genres:
            if g in genre_movies:
                genre_movies[g].append(movieid)
            else:
                genre_movies[g] = [movieid]

    #     if (len(movies) % 500) == 0:
    #         cursor = db.cursor()
    #         try:
    #             cursor.executemany(insert_sql, movies)
    #         except:
    #             print movies

    #         db.commit()
    #         print(cursor.rowcount, "inserted")
    #         movies = []
    #         cursor.close()
    
    # if len(movies) > 0:
    #     cursor = db.cursor()
    #     cursor.executemany(insert_sql, movies)
    #     db.commit()
    #     print(cursor.rowcount, "inserted")
    #     cursor.close()

    genres_sql = "INSERT INTO genres (genreid, name, count) VALUE (%s, %s, %s)"

    genres_counts = [(g, len(genre_movies[g])) for g in genre_movies]
    ids_genres = []
    for i in range(1, len(genres_counts)+1):
        ids_genres.append(
            (i, genres_counts[i-1][0], genres_counts[i-1][1])
        )

    cursor = db.cursor()
    cursor.executemany(genres_sql, ids_genres)
    db.commit()
    print(cursor.rowcount, "inserted")
    cursor.close()

    genre_movies_sql = "INSERT INTO genres_movies (genreid, movieid) VALUE (%s, %s)"
    genres_ids = dict(zip([g for (g,c) in genres_counts], range(1, len(genres_counts)+1)))
        
    cursor = db.cursor()

    for g in genre_movies:
        print "setting", g
        i = 0
        for movieid in genre_movies[g]:
            cursor.execute(genre_movies_sql, (genres_ids[g], movieid))
            i += 1
            if (i % 100) == 0:
                db.commit()
                print i
        db.commit()


def parse_ratings(db, rfile):
    ratings = []
    rcsv = csv.DictReader(rfile)

    ratings_sql = "INSERT INTO ratings (movieid, userid, rating, ts) VALUES (%s,%s,%s,%s)"

    for row in rcsv:
        movieid = int(row['movieId'])
        userid = int(row['userId'])
        rating = float(row['rating'])
        ts = datetime.fromtimestamp(float(row['timestamp']))

        ratings.append(
            (movieid,userid,rating,ts)
        )

        if (len(ratings) % 500) == 0:
            cursor = db.cursor()
            cursor.executemany(ratings_sql, ratings)
            db.commit()
            print(cursor.rowcount, "inserted")
            cursor.close()
            ratings = []
    
    if len(ratings) > 0:
        cursor = db.cursor()
        cursor.executemany(ratings_sql, ratings)
        db.commit()
        print(cursor.rowcount, "inserted")
        cursor.close()


def parse_links(db, lfile):
    lcsv = csv.DictReader(lfile)
    links_sql = "UPDATE movies SET tmdb=%s, imdb=%s, poster=%s WHERE movieid=%s"

    cursor = db.cursor()
    for row in lcsv:
        vals = (
            row['tmdb'],
            row['imdb'],
            row['poster'],
            int(row['movieid'])
        )
        cursor.execute(links_sql, vals)
    db.commit()
    cursor.close()


def main():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="movielens",
        passwd="movielens",
        database="movielens"
    )

    # create_tables(db)

    # with open(sys.argv[1]) as mfile:
    #     parse_movies(db, mfile)

    with open(sys.argv[2]) as rfile:
        parse_ratings(db, rfile)

    # with open(sys.argv[3]) as lfile:
    #     parse_links(db, lfile)

if __name__ == "__main__":
    main()
    