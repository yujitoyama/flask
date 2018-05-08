from flask import Flask, render_template #追加
from flask import request
from pymongo import MongoClient
import sqlite3
from contextlib import closing

app = Flask(__name__)
dbname = 'database.db'

@app.route('/')
def hello():
    name = "shoki"
    #return name
    return render_template('hello.html', title='flask test', name=name) #変更

@app.route('/post', methods=['POST']) #Methodを明示する必要あり
def hellopost():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = "no name."

    #mongoDB
    client = MongoClient('localhost', 27017)
    db = client.test_database
    collection = db.test_collection
    print(collection.find_one({"author": "Mike"},{"tags":1,"_id":0}))

    #sqlite
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        # executeメソッドでSQL文を実行する
        create_table = '''create table users (id int, name varchar(64),
                          age int, gender varchar(32))'''
        c.execute(create_table)

        # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
        # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
        # タプルで渡す．
        sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
        user = (1, name, 20, 'male')
        c.execute(sql, user)

        # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
        # executemanyメソッドを実行する
        insert_sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
        users = [
            (2, 'Shota', 54, 'male'),
            (3, 'Nana', 40, 'female'),
            (4, 'Tooru', 78, 'male'),
            (5, 'Saki', 31, 'female')
        ]
        c.executemany(insert_sql, users)
        conn.commit()

        select_sql = 'select * from users'
        for row in c.execute(select_sql):
            print(row)

    return render_template('hello.html', title='flask test', name=name) 

## おまじない
if __name__ == "__main__":
    app.run(debug=True)