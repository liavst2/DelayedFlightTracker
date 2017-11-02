#############################################################
# FILE: main.py
# EXERCISE : A needle in a data haystack - final project
#############################################################


import Parser
import pandas
import sqlite3 as sql


def main():
    """
    main function.
    From here we made jsons out of our database
    :return: nothing
    """

    query = """
            select distinct Description as name, count(*) as size
            from flights join airports on ORIGIN_AIRPORT_ID = Code
            group by name
            order by size
            """


    title = """
            airports_to_sizes
            """

    try:
        Parser.jsonify(query.strip(), title.strip())
    except:
        print("Ata lo yatziv.")
    finally:
        exit(0)


def merge():
    """
    This function was used to convert csv file to .db file
    :return: nothing. Only changes flights.db database
    """
    # this maintains a connection to our database
    con = sql.connect("dataset/flights.db")
    # now loop over all csv's (each one represents one month of the year
    for i in range(1, 13):
        # read the csv file
        df = pandas.read_csv("dataset/f_%d.csv" % i)
        # convert it to database
        df.to_sql("days", con, if_exists="append")


if __name__ == "__main__":
    merge()
    main()
