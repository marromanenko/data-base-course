import psycopg2


def makeConnect():
    return psycopg2.connect(
        user="postgres",
        password="qwerty",
        host="localhost",
        port="5432",
        database="postgres",
    )


def closeConnect(connection):
    connection.commit()
    connection.close()
