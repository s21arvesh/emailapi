from flask import g, current_app as app
import pymysql
from sqlalchemy import create_engine
# this is the change

def get_db():
    if 'db' not in g:
        g.db = {}
        return connect_to_database()


def connect_to_database():
    con = pymysql.connect(host=app.config["DB_SERVER"], user=app.config["DB_USERNAME"],
                          password=app.config["DB_PASSWORD"], db=app.config["DB_NAME"],
                          cursorclass=pymysql.cursors.
                          DictCursor, port=app.config["DB_PORT"], autocommit=True)
    print(type(con))

    cur = con.cursor()

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"
                           .format(host=app.config["DB_SERVER"], user=app.config["DB_USERNAME"],
                                   pw=app.config["DB_PASSWORD"], db=app.config["DB_NAME"],
                                   port=app.config["DB_PORT"]))

    g.db['dbConnObj'] = con
    g.db['dbConnCur'] = cur
    g.db['dbConnEnf'] = engine
    return


def close_db_conn():
    db = g.pop('db', None)
    print(db)
    if db is not None:
        db['dbConnCur'].close()
        db['dbConnObj'].close()
    return
