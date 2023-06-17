import mysql.connector
import json


def create_database(db_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )

    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()
    connection.close()


def connect_to_database(db_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database=db_name
    )

    return connection


def create_table(connection):
    cursor = connection.cursor()
    exists_query = f"SHOW TABLES LIKE 'movements'"
    cursor.execute(exists_query)

    exists = cursor.fetchone() is not None

    if not exists:
        create_table_query = """
                CREATE TABLE IF NOT EXISTS movements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data JSON
                )
            """
        functions_dict = {
            "Left Click": "right_wolf",
            "Double Click": "right_metal",
            "Right Click": "right_gun_finger",
            "Scroll": "right_scout",
            "Paste": "left_wolf",
            "Copy": "left_gun_finger",
            "Cut": "left_scissors"
        }
        cursor.execute(create_table_query)
        insert_dictionary(connection, functions_dict)
    cursor.close()


def check_dictionary_exists(connection, dictionary):
    cursor = connection.cursor()
    select_query = "SELECT COUNT(*) FROM movements WHERE data = %s"
    data_json = json.dumps(dictionary)
    cursor.execute(select_query, (data_json,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


def insert_dictionary(connection, dictionary):
    if not check_dictionary_exists(connection, dictionary):
        cursor = connection.cursor()
        insert_query = "INSERT INTO movements (data) VALUES (%s)"
        data_json = json.dumps(dictionary)
        cursor.execute(insert_query, (data_json,))
        connection.commit()
        cursor.close()


def delete_first_row(connection):
    cursor = connection.cursor()
    select_query = "SELECT id FROM movements LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()

    if result is not None:
        first_row_id = result[0]
        delete_query = f"DELETE FROM movements WHERE id = {first_row_id}"
        cursor.execute(delete_query)
        connection.commit()
        print("First row deleted.")
    else:
        print("No rows found in the table.")

    cursor.close()


def fetch_dictionaries(connection):
    cursor = connection.cursor()
    select_query = "SELECT data FROM movements"
    cursor.execute(select_query)
    dictionaries = []
    for (data,) in cursor:
        dictionary = json.loads(data)
        dictionaries.append(dictionary)
    cursor.close()
    return dictionaries[0]


def configuration():
    # Main code execution
    database_name = "handy_schema"

    # Create the database if it doesn't exist
    create_database(database_name)

    # Connect to the database
    connection = connect_to_database(database_name)

    # Create a table if it doesn't exist
    create_table(connection)

