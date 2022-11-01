from datetime import date
from flask import Flask, request
from flask_restful import Api
import sqlite3
import conf

DATABASE = conf.PATH

app = Flask(__name__)
api = Api()


@app.route('/v1/user')
def user():
    id = request.args['id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT phone, login, name, birth, tg, email FROM users WHERE id = {id}')
        r = cursor.fetchall()
        print(r)
        if len(r) == 0:
            raise Exception(f'Пользователь c id = {id} не зарегистрирован.')
        r = list(*r)
        response = {
                    'phone': r[0],
                    'login': r[1],
                    'name': r[2],
                    'birth': r[3],
                    'tg': r[4],
                    'email': r[5]
        }
    except Exception as exc:
        response = {
            'code': 409,
            'text': f'{exc}'
        }
    cursor.close()
    return response


@app.route('/v1/auth/register', methods=['POST'])
def register():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        for val in data:
            if len(data[val]) == 0 and val != 'tg' and val != 'email':
                raise Exception(f'Нет данных в обязательном поле {val}')
        l = data['birth'].split("-")
        y = int(l[0])
        m = int(l[1])
        d = int(l[2])
        ln = (str(date.today())).split("-")
        yn = int(ln[0]) - 18
        mn = int(ln[1])
        dn = int(ln[2])
        if date(y, m, d) > date(yn, mn, dn):
            raise Exception(f'Несовершеннолетний пользователь, в регистрации отказано!')

        cursor.execute('INSERT INTO users (phone, login, password, name, birth, tg, email) VALUES (?, ?, ?, ?, ?, '
                           '?, ?)', (data["phone"], data["login"], data["password"], data["name"], data["birth"],
                                     data["tg"], data["email"]))
        conn.commit()
        cursor.execute('SELECT id FROM users ORDER BY -id LIMIT 1')
        a = cursor.fetchall()
        (r, ) = a
        r = r[0]
        response = {
            'id': r
        }

    except Exception as exc:
        response = {
            'code': 409,
            'text': f'{exc}'
        }
    cursor.close()
    return response


@app.route('/v1/auth/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        for val in data:
            if len(data[val]) == 0:
                raise Exception(f'Нет данных в обязательном поле {val}')
        cursor.execute(f'SELECT id FROM users WHERE login = "{data["login"]}" AND password = "{data["password"]}"')
        r = cursor.fetchone()
        if r is None:
            raise Exception('Пользователь с такой парой логин/пароль не зарегистрирован.')
        response = {
            'id': r[0]
        }
    except Exception as exc:
        response = {
            'code': 409,
            'text': f'{exc}'
        }
    cursor.close()
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="127.0.0.1")

