import psycopg2
import psycopg2.extras
import os
import collections
import json


def create_json_file(result, upload_folder):
    #fligths_result = json.dumps(flight_list)
    try:
        "Creating json file"
        with open(os.path.join(upload_folder, "flights.json"), 'w') as outfile:
            json.dump(result, outfile)
    except:
        print "Failed creating json file..."
        raise


def close_db(conn):
    conn.close()
    print('Database connection closed.')


def make_query(conn, statement):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print "Executing query ..."
        cur.execute(statement)
    except:
        print "Failed executing query..."
        raise

    resultset = cur.fetchall()
    dict_result = []
    for row in resultset:
        dict_result.append(dict(row))
    return dict_result


def connect_db(user, password):
    # Try to connect
    try:
        conn = psycopg2.connect(dbname='flights', user=user, password=password)
        print "Database connection started."
        return conn
    except:
        raise


def main():
    USER = "aguijarro"
    PASSWORD = "aguijarro"
    UPLOAD_FOLDER = os.path.realpath('.') + '/data'

    # Make database connection
    conn = connect_db(USER, PASSWORD)
    # Query Data
    statement = "select month, count(flight_num) total from flights group by month;"
    result = make_query(conn, statement)
    # Create json file
    create_json_file(result, UPLOAD_FOLDER)
    # Close database connection
    close_db(conn)

if __name__ == '__main__':
    main()