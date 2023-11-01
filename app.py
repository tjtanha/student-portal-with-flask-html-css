from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL




app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'studdent_info'
  # To get the results in dictionary format
mysql = MySQL(app)




app.secret_key = 'some_secret_key_for_sessions'


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin1' and password == '1234':
            return redirect(url_for('welcome'))
        else:
            flash('Incorrect username or password')
    return render_template('admin_login.html')



@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        s_id = request.form['s_id']
        s_name = request.form['s_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(s_id, s_name) VALUES (%s, %s)", (s_id, s_name))
        mysql.connection.commit()
        flash("User added successfully!")
        return redirect('/')
    return render_template('index.html')


@app.route('/update_page', methods=['GET'])
def update_page():
    s_id = request.args.get('s_id', None)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE s_id=%s", [s_id])
    student = cur.fetchone()
    return render_template('update.html', student=student)

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        s_id = request.form['s_id']
        s_name = request.form['s_name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET s_name=%s WHERE s_id=%s", (s_name, s_id))
        mysql.connection.commit()
        if cur.rowcount == 0:
            flash("No student found with the given ID!")
        else:
            flash("Student name updated successfully!")
        return redirect('/update_page')



@app.route('/delete_page', methods=['GET'])
def delete_page():
    s_id = request.args.get('s_id', None)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE s_id=%s", [s_id])
    student = cur.fetchone()
    return render_template('delete.html', student=student)
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        s_id = request.form['s_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE s_id=%s", [s_id])
        mysql.connection.commit()
        if cur.rowcount == 0:
            flash("No student found with the given ID!")
        else:
            flash("Student deleted successfully!")
        return redirect('/delete_page')


@app.route('/display')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('display.html', students = users)



if __name__ == '__main__':
    app.run(debug=True)
