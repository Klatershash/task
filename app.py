from flask import Flask, render_template, request, session, redirect
import db
import time
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'qklasnflkqj3ijfaklfasjnf.nqw;foqwfnajlfkansfjklhuo82'

db.create_tables()

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session['login']
    limit = db.select_limit_user(user)
    error = ''

    suc = ''
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_end = request.form.get('date_end')


        date_start = time.strftime('%Y-%m-%d %H:%M:%S')
        if limit == 0:
            error = 'Ваш лимит исчерпан'
        else:
            limit -= 1
            db.insert_task(title,description,date_start,user,date_end,limit,user)
            suc = 'Вы успешно добавили задачу'
    tasks = db.select_tasks(user)
    tasks_new = []
    current_datetime = datetime.now()
    timestap_current = int(time.mktime(current_datetime.timetuple()))

    for task in tasks:
        date_end_time = datetime.strptime(task[-2], "%Y-%m-%dT%H:%M")
        timestap = int(time.mktime(date_end_time.timetuple()))

        a = []
        a.append(task[0])
        a.append(task[1])
        if task[2] == 'Завершен':
            a.append('Завершен')
        else:
            if datetime.fromisoformat(task[-2]) < current_datetime:
                a.append('Просрочена')
            else:
                a.append('В работе')
        a.append(task[3])
        a.append(task[4])
        a.append(task[5])
        a.append(task[6])
        res_time = timestap - timestap_current
        days = res_time // (24 * 3600) #25/3
        res_time %= (24 * 3600)
        hours = res_time // 3600
        res_time %= 3600
        minutes = res_time // 60
        seconds = res_time % 60
        res_str_date = ''
        if days < 0 or hours < 0 or minutes < 0 or seconds < 0 or task[2] == 'Завершен':
            res_str_date = '0'
        else:
            res_str_date =  f'Дни: {days} Часы: {hours} Минуты: {minutes} Секунды {seconds}'


        a.append(res_str_date)

        tasks_new.append(a)

        print(res_time)
    print(tasks_new)

    return render_template('profile.html', suc=suc, tasks=tasks_new, error=error, limit=limit)


@app.route('/reg', methods=['GET', 'POSt'])
def reg():
    suc = ''
    errors = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if db.authLogin(login):
            errors += 'Такой логин уже существует!'
        else:
            db.addUser(login, password)
            suc += 'Вы успешно зарегистрированы'
    return render_template('reg.html', errors=errors, suc=suc)

@app.route('/auth', methods=['GET', 'POSt'])
def auth():
    errors = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if db.authLoginPassword(login, password):
            session['login'] = login
            return redirect('/profile')
        else:
            errors += 'Error login or password'

    return render_template('auth.html', errors=errors)


@app.route('/logout')
def logout():
    if 'login' in session:
        del session['login']
    return redirect('/')

@app.route('/action', methods=['POSt'])
def action():
    if request.method == 'POST':
        id_task = request.form.get('id_task')
        if 'delete' in request.form:
            db.delete_task_id(id_task)
        if 'finish' in request.form:
            db.update_task_id(id_task)
    return redirect('/profile')

@app.route('/edit_anwer', methods=['POST'])
def edit_anwer():
    if request.method == 'POST':
        id_task = request.form.get('id_task')
        answer = request.form.get('answer')
        db.update_task_anwer(id_task, answer)
    return redirect('/profile')
app.run(debug=True)