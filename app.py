from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

app = Flask(__name__, template_folder='frontend')

def addData(connection, cursor):
    csv_data = pd.read_csv('https://raw.githubusercontent.com/yasseriz/crispy-octo-barnacle/main/Books.csv', index_col=False, encoding="ISO-8859-1", dtype={
                           "ISBN": str, "Book-Title": str, "Book-Author": str, "Year-Of-Publication": int, "Image-URL-L": str})

    for i, row in csv_data.iterrows():
        sql = "INSERT INTO Book VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()

def randomMovie(cursor):
    cursor = connection.cursor()
    sql_random_query = "SELECT * FROM Book ORDER BY RAND() LIMIT 1"
    cursor.execute(sql_random_query)
    result = cursor.fetchone()
    return result

try:
    connection = mysql.connector.connect(host=os.environ.get('host'),
                                         database=os.environ.get('database'),
                                         user=os.environ.get('user'),
                                         password=os.environ.get('password'),
                                         port=os.environ.get('port'))

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Connected to database:", record)

        cursor.execute('DROP TABLE IF EXISTS Book')

        sql_select_Query = "create TABLE Book(ISBN varchar(15) NOT NULL, Book varchar(100) NOT NULL, Author varchar(50) NOT NULL, Year int unsigned, Image varchar(100), PRIMARY KEY(ISBN)) "
        cursor.execute(sql_select_Query)
        print("Book table created")

        addData(connection, cursor)
        print("Records inserted")

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):

        sql_select_Query = ("SELECT * FROM Book ORDER BY RAND() LIMIT 1")
        cursor.execute(sql_select_Query)
        result = cursor.fetchall()
        for i in result:
            print(i)

        # connection.close()
        cursor.close()
        print("MySQL connection is closed")

# Root URL
@app.route('/', methods=['GET','POST'])
def home():
    if request.method =="POST":
        result = randomMovie(cursor)
        print(type(result))
        return render_template('main.html', result=result)
    return render_template('main.html')

# if (__name__ == "__main__"):
#      app.run(port = 5000)
