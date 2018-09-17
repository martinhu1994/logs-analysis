import psycopg2
import calendar


def report_one(cursor):
    cursor.execute("\
        SELECT articles.title, articleviews.views \
        FROM articles JOIN articleviews ON articles.slug = articleviews.slug \
        ORDER BY articleviews.views DESC \
        LIMIT 3")
    result = cursor.fetchall()
    for entry in result:
        print("\"%s\" -- %d views" % (entry[0], entry[1]))


def report_two(cursor):
    cursor.execute("\
        SELECT final.name AS name, sum(final.views) AS views\
        FROM(\
            (articles JOIN articleviews \
            ON articles.slug = articleviews.slug) AS sub \
        JOIN authors \
        ON sub.author = authors.id) AS final \
        GROUP BY name \
        ORDER BY views DESC")
    result = cursor.fetchall()
    for entry in result:
        print("%s -- %d views" % (entry[0], entry[1]))


def report_three(cursor):
    cursor.execute("\
        SELECT final.date1, (final.error * 1.0) / (final.total * 1.0) \
        FROM( \
            (SELECT date_trunc('day', time) AS date1, count(*) AS total \
            FROM log \
            GROUP BY date1) sub1 \
        JOIN \
            (SELECT date_trunc('day', time) AS date2, count(*) AS error \
            FROM log \
            WHERE status != '200 OK' \
            GROUP BY date2) sub2 \
        ON sub1.date1 = sub2.date2) final \
        WHERE ((final.error * 1.0) / (final.total * 1.0)) > 0.01")
    result = cursor.fetchall()
    for entry in result:
        month = calendar.month_name[entry[0].month]
        day = entry[0].day
        year = entry[0].year
        percent = entry[1] * 100
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
