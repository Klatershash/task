import sqlite3 #mysql postgresql

def connect():
    conn = sqlite3.connect('data.db')
    return conn

def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists users(
            id integer primary key autoincrement,
            login text not null,
            password text not null,
            email text
        )
    ''')
    cursor.execute('''
            create table if not exists tasks(
                id integer primary key autoincrement,
                title text not null,
                status text,
                description text,
                date_start text,
                user text,
                data_end text
            )
        ''')
    conn.commit()


def insert_task(title, description, date_start, user, data_end, limit, login):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('insert into tasks (title, status, description, date_start, user, data_end) values (?,"в работе", ?, ?, ?, ?)', (title,description, date_start, user, data_end))
    conn.commit()


    cursor.execute('update users set limit1 = ? where login = ?', (int(limit), login))
    conn.commit()

def authLogin(login):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '"+login+"'")
    return cursor.fetchone()

def addUser(login, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into users (login,password) values ('"+login+"', '"+password+"')")
    conn.commit()


def authLoginPassword(login,password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '"+login+"' and password = '"+password+"'")
    return cursor.fetchone()

def select_tasks(login):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('select * from tasks where user = ? order by data_end desc', (login,))
    return cursor.fetchall()

def select_limit_user(login):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('select * from users where login = ? ', (login,))
    return cursor.fetchone()[-1]


def delete_task_id(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('delete from tasks where id = ?', (id,))
    conn.commit()

def update_task_id(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('update tasks set status = "Завершен" where id = ?', (id,))
    conn.commit()

def update_task_anwer(id, answer):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('update tasks set answer = ? where id = ?', (answer,id))
    conn.commit()