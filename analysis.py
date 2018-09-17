#!/usr/bin/env python

import psycopg2
import calendar


def report_one(cursor):
    ''' Find the most popular three articles of all time. '''

    try:
        cursor.execute('''
            SELECT articles.title, articleviews.views
            FROM articles JOIN articleviews ON articles.slug=articleviews.slug
            ORDER BY articleviews.views DESC
            LIMIT 3''')
    except psycopg2.Error as e:
        print(e.pgerror)

    result = cursor.fetchall()
    for title, view in result:
        print("\"%s\" -- %d views" % (title, view))


def report_two(cursor):
    ''' List authors by the popularity of their articles. '''

    try:
        cursor.execute('''
            SELECT final.name AS name, sum(final.views) AS views
            FROM(
                (articles JOIN articleviews
                ON articles.slug = articleviews.slug) AS sub
            JOIN authors
            ON sub.author = authors.id) AS final
            GROUP BY name
            ORDER BY views DESC''')
    except psycopg2.Error as e:
        print(e.pgerror)

    result = cursor.fetchall()
    for author, view in result:
        print("%s -- %d views" % (author, view))


def report_three(cursor):
    ''' Find the days that more than 1% of requests lead to errors. '''

    try:
        cursor.execute('''
            SELECT final.date1, (final.error * 1.0) / (final.total * 1.0)
            FROM(
                (SELECT date_trunc('day', time) AS date1, count(*) AS total
                FROM log
                GROUP BY date1) sub1
            JOIN
                (SELECT date_trunc('day', time) AS date2, count(*) AS error
                FROM log
                WHERE status != '200 OK'
                GROUP BY date2) sub2
            ON sub1.date1 = sub2.date2) final
            WHERE ((final.error * 1.0) / (final.total * 1.0)) > 0.01''')
    except psycopg2.Error as e:
        print(e.pgerror)

    result = cursor.fetchall()
    for date, ratio in result:
        month = calendar.month_name[date.month]
        day = date.day
        year = date.year
        percent = ratio * 100
        print("%s %d, %d -- %.1f%% errors" % (month, day, year, percent))


if __name__ == "__main__":
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()

    print("Report One: ")
    report_one(cursor)
    print("")

    print("Report Two: ")
    report_two(cursor)
    print("")

    print("Report Three: ")
    report_three(cursor)
    print("")

    db.close()
