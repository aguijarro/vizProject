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

    year_st = "select year, count(id) total \
               from flights group by year;"

    year_rt = make_query(conn, year_st)

    month_st = "select month, count(id) total \
                 from flights group by month;"
    month_rt = make_query(conn, month_st)

    day_month_st = "select day_of_month, count(id) total \
                 from flights group by day_of_month;"
    day_month_rt = make_query(conn, day_month_st)


    day_week_st = "select day_of_week, count(id) total \
                   from flights group by day_of_week;"
    day_week_rt = make_query(conn, day_week_st)

    carrier_year_st = "(select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2000'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2001'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2002'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2003'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2004'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2005'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2006'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2007'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5)\
                        UNION\
                        (select f.year, c.description, count(f.id) total\
                        from flights f, carriers c\
                        where f.unique_carrier = c.code\
                        and f.year = '2008'\
                        group by f.year, c.description\
                        order by count(f.id) desc\
                        limit 5);"
    carrier_year_rt = make_query(conn, carrier_year_st)

    top5_carriers_rs = "select c.description, count(f.id) total\
                       from flights f, carriers c\
                       where f.unique_carrier = c.code\
                       group by c.description\
                       order by count(f.id) desc\
                       limit 5"

    top5_carriers_rt = make_query(conn, top5_carriers_rs)

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


    year_cancelled_st = "select f.year, f.cancelled, count(f.id) total\
                         from flights f\
                         group by f.year, f.cancelled;"

    year_cancelled_rt = make_query(conn, year_cancelled_st)


    year_cancelled_code_st = "select f.year, f.cancellation_code, count(f.id) total\
                              from flights f\
                              group by f.year, f.cancellation_code;"

    year_cancelled_code_rt = make_query(conn, year_cancelled_code_st)


    cancelled_code_st = "select f.cancellation_code, count(f.id) total\
                         from flights f\
                         group by f.cancellation_code;"

    cancelled_code_rt = make_query(conn, cancelled_code_st)


    cancelled_st = "select f.cancelled, count(f.id) total\
                    from flights f\
                    group by f.cancelled;"

    cancelled_rt = make_query(conn, cancelled_st)

    #Create json file
    create_json_file(year_rt, UPLOAD_FOLDER, "year_flights.json")
    create_json_file(month_rt, UPLOAD_FOLDER, "month_flights.json")
    create_json_file(day_month_rt, UPLOAD_FOLDER, "day_months_flights.json")
    create_json_file(day_week_rt, UPLOAD_FOLDER, "day_week_flights.json")
    create_json_file(carrier_year_rt, UPLOAD_FOLDER, "carrier_year.json")
    create_json_file(carrier_year_rt, UPLOAD_FOLDER, "top5_carriers.json")
    create_json_file(airport_rt, UPLOAD_FOLDER, "airports.json")
    create_json_file(top25_airport_rt, UPLOAD_FOLDER, "top25_airports.json")
    create_json_file(year_cancelled_rt, UPLOAD_FOLDER, "year_cancelled.json")
    create_json_file(year_cancelled_code_rt, UPLOAD_FOLDER, "year_cancelled_code.json")
    create_json_file(cancelled_code_rt, UPLOAD_FOLDER, "cancelled_code.json")
    create_json_file(cancelled_rt, UPLOAD_FOLDER, "cancelled.json")

    # Close database connection
    close_db(conn)

if __name__ == '__main__':
    main()
