import psycopg2
import psycopg2.extras
import os
import collections
import json


def create_json_file(result, upload_folder, name):
    #fligths_result = json.dumps(flight_list)
    try:
        "Creating json file"
        with open(os.path.join(upload_folder, name), 'w') as outfile:
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
    statement = "select month, count(flight_num) total \
                 from flights group by month;"
    result = make_query(conn, statement)

    airport_st = "select iata, airport, city, state, lat, long\
                  from airports\
                  where country = 'USA'\
                  and iata not in ('ABO', 'BQN', 'CPX',\
                  'FAQ', 'GRO', 'GSN', 'GUM', 'MAZ',\
                  'PPG', 'PR03', 'PSE', 'SIG', 'SJU',\
                  'STT', 'STX', 'TNI', 'TT01', 'VQS',\
                  'X63', 'X6','X67', 'X95', 'X96', 'Z08',\
                  'X66');"

    airport_rt = make_query(conn, airport_st)

    #Returns que top25 airports by number of figths
    top25_airport_st = "select a.iata, a.airport, a.city, a.state, a.lat,\
                        a.long, f.year, count(f.id) flights\
                        from airports a, flights f\
                        where a.iata = f.origin\
                        and f.origin in ('ATL','ORD','DFW','LAX','PHX',\
                        'IAH','DEN','LAS','DTW','MSP','EWR','SFO','BOS',\
                        'SLC','CLT','LGA','CVG','PHL','MCO','SEA','BWI',\
                        'STL','IAD','DCA','JFK')\
                        group by a.iata, a.airport, a.city, a.state, a.lat,\
                        a.long, f.year;"

    top25_airport_rt = make_query(conn, top25_airport_st)

    # Create json file
    create_json_file(result, UPLOAD_FOLDER, "flights.json")
    create_json_file(airport_rt, UPLOAD_FOLDER, "airports.json")
    create_json_file(top25_airport_rt, UPLOAD_FOLDER, "top25_airports.json")
    # Close database connection
    close_db(conn)

if __name__ == '__main__':
    main()
