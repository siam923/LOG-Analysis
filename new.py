#Language - Python 2
import psycopg2

"""
Views:
1->create view map as select authors.name,articles.slug
from authors join articles on articles.author = authors.id;

2->  create view visit as select time::date as day,status from log;

3-> create view performance as select v.day,v.requests,f.error
    from (select day,count(status) as error
    from visit where status like ('%404%') group by day)
    f join (select day,count(status) requests from visit group by day) v
        on  v.day = f.day;

"""

def connect(db_name = 'news'):
    return psycopg2.connect(dbname = db_name)

def execute_query(query):
    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results

def most_popular_articles():
    query = """
        select articles.title, count(log.path) visits
            FROM articles join log
        on log.path LIKE('%' || articles.slug)
        where log.status like '%200%'
        group by log.path,articles.title
        order by visits DESC limit 3;
    """
    result = execute_query(query)
    print "1.What are the most popular three articles of all time?"
    for article,view in result:
        print "\"  {}\" - {} views".format(article,view)


def most_popular_authors():
    # Map is the view name
    query = """
        select map.name , count(log.path)
            from map join log on log.path like ('%'|| map.slug)
        group by map.name
        order by count(log.path) desc limit 3;
    """
    result = execute_query(query)
    print "2.Who are the most popular article authors of all time?"
    for author,view in result:
        print "  {} - {} views".format(author,view)

def error_date():
    query = """
        select to_char(day,'FMMonth DD,YYYY'),100*cast(error as float)/cast(requests as float) error
            from performance
        where requests/100 < error;
    """
    print "3.On which days did more than 1% of requests lead to errors?"
    result = execute_query(query)
    for day,error in result:
        print "  {} - {}% errors".format(day,round(error,2))

if __name__ == '__main__':
    most_popular_articles()
    print ""
    most_popular_authors()
    print ""
    error_date()
