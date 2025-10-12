import sqlite3, hashlib, os

from flask import Flask, request, redirect, render_template, session

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


def user_data():
    con = sqlite3.connect('Пользователи.db')
    cur = con.cursor()
    if 'email' not in session:
        info = None
    else:
        cur.execute("SELECT name, address, phone FROM users WHERE email = '" + session['email'] + "'")
        info = cur.fetchone()
    con.close()
    return info


@app.route("/")
def redir():
    return redirect("/main")


@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        if 'email' in session:
            user = user_data()[0]
            prodName = request.form['prodName']
            prodPrice = request.form['prodPrice']
            prodPic = request.form['prodPic']
            con1 = sqlite3.connect('Заказ.db')
            cur = con1.cursor()
            cur.execute('''INSERT INTO kart (user, prodName, prodPrice, prodPic) VALUES (?, ?, ?, ?)''',
                         (user, prodName, prodPrice, prodPic))
            con1.commit()
        else:
            return redirect('/login')
    return render_template("/main_page.html")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    con = sqlite3.connect('Пицца.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM food''')
    response1 = cur.fetchall()
    print(response1)
    con.close()
    if request.method == "POST":
        if 'email' in session:
            user = user_data()[0]
            prodName = request.form['prodName']
            prodPrice = request.form['prodPrice']
            prodPic = request.form['prodPic']
            con1 = sqlite3.connect('Заказ.db')
            cur = con1.cursor()
            cur.execute('''INSERT INTO kart (user, prodName, prodPrice, prodPic) VALUES (?, ?, ?, ?)''',
                         (user, prodName, prodPrice, prodPic))
            con1.commit()
        else:
            return redirect('/login')
    return render_template("/menu.html", pizzalist=response1)


@app.route("/contacts")
def contacts():
    return render_template("/contacts.html")


@app.route("/discount")
def discount():
    return render_template("/discount.html")


@app.route("/order")
def order():
    return render_template("/order.html")


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect('/main')
    else:
        return render_template('login.html', error='')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'email' in session:
        return redirect('/main')
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if is_valid(email, password):
                session['email'] = email
                session.permanent = True
                return redirect('/main')
            else:
                error = 'Invalid UserId / Password'
                return render_template('login.html', error=error)
    return render_template('login.html', error='')


@app.route("/logout")
def logout():
    session.pop('email', None)
    con = sqlite3.connect('Заказ.db')
    cur = con.cursor()
    cur.execute('''DELETE FROM kart''')
    con.commit()
    return redirect('/main')


def is_valid(email, password):
    con = sqlite3.connect('Пользователи.db')
    cur = con.cursor()
    cur.execute('SELECT name, email, psw FROM users')
    data = cur.fetchall()
    for row in data:
        if row[1] == email and row[2] == hashlib.md5(password.encode()).hexdigest():
            print(row[0])
            return True
    return False


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        cpass = request.form['cpassword']
        if cpass == password:
            con = sqlite3.connect('Пользователи.db')
            cur = con.cursor()
            cur.execute('INSERT INTO users (name, phone, address, email, psw) VALUES (?, ?, ?, ?, ?)',
                         (name, phone, address, email, hashlib.md5(password.encode()).hexdigest(),))
            con.commit()
            return redirect("/login")
        else:
            error = 'Invalid UserId / Password'
            return render_template("register.html", error=error)
    return render_template("register.html")


@app.route("/comments", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        con = sqlite3.connect('Отзывы.db')
        cur = con.cursor()
        cur.execute('''SELECT * FROM comments''')
        response1 = cur.fetchall()
        print(response1)
        con.close()
    if request.method == "POST":
        con = sqlite3.connect('Отзывы.db')
        cur = con.cursor()
        content = request.form['content']
        if 'email' not in session:
            cur.execute('''INSERT INTO comments (user, content) VALUES (?,?)''', ('Гость', content,))
        else:
            name = user_data()[0]
            cur.execute('''INSERT INTO comments (user, content) VALUES (?,?)''', (name, content,))
        con.commit()
        con.close()
        return redirect('/comments')
    return render_template('comments.html', commentdata=response1, session=session)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'email' not in session:
        return redirect('/login')
    else:
        name = user_data()[0]
        address = user_data()[1]
        phone = user_data()[2]
        return render_template('profile.html', name=name, address=address, phone=phone)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    con = sqlite3.connect('Заказ.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM kart''')
    orderlist = cur.fetchall()
    con.commit()
    return render_template('cart2.html', orderlist=orderlist)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    con = sqlite3.connect('Заказ.db')
    cur = con.cursor()
    cur.execute('''DELETE FROM kart''')
    con.commit()
    return redirect("/cart")


if __name__ == "__main__":
    app.run(debug=True)

