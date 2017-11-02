#############################################################
# FILE: Parser.py
# EXERCISE : A needle in a data haystack - final project
#############################################################


import sqlite3 as sql
import json as js


DB = "dataset/flights.db"


def execute_query(query):
    """
    Executes query on our database
    :param query: the query to execute
    :return: the resulted rows and the names of the columns
    """
    cursor = sql.connect(DB).cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    names = list(map(lambda x: x[0], cursor.description))
    return result, names


def json_open(title):
    """
    Opens json file for writing.
    :param title: the name of the file
    :return: the file descriptor
    """
    jsf = open("jsons/%s.json" % title, "w+")
    jsf.write("\n")
    return jsf


def jsonify(query, title):
    """
    Parses sql query into json file.
    :param query: the query to execute
    :param title: the name of the json file
    :return: the parsed json file
    """
    sql_result, columns = execute_query(query)
    try:
        jsf = json_open(title)
    except IOError:
        raise
    wrapper = {}
    for idx, row in enumerate(sql_result):
        current = {}
        for i in range(len(columns)):
            current[columns[i]] = row[i]
        wrapper[str(idx)] = current
    jsf.write(js.dumps(wrapper, sort_keys=True, indent=6, separators=(',', ': ')))
    jsf.write("\n")
    return jsf
