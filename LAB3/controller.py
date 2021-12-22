import psycopg2


def makeConnect():
    return psycopg2.connect(
        user="postgres",
        password="qwerty",
        host="localhost",
        port="5432",
        database="database",
    )


def closeConnect(connection):
    connection.commit()
    connection.close()
