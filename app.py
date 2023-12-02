from flask import Flask, flash,render_template, request, redirect, url_for, session
from forms import loginForm, AddBook, signUpForm
import MySQLdb
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'LibraryDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# @app.route("/add_member")
# def add_member():

# @app.route("/member")
# def members():

# @app.route("/delete/<string:id>")
# def delete_book():


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    form = AddBook(request.form)
    if request.method == "POST" and form.validate():
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT id FROM books WHERE id=%s", [form.id.data])
        book = cur.fetchone()
        if(book):
            error = "Id da ton tai"
            return render_template('add_book.html', form=form, error=error)
        cur.execute("INSERT INTO books (id,title,author,category,publication_date,num_pages,available_quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.category.data,
            form.publication_date.data,
            form.num_pages.data,
            form.available_quantity.data,
        ])
        mysql.connection.commit()

        # Close DB Connection
        cur.close()
        # Flash Success Message
        flash("New Book Added", "success")
        # Redirect to show all books
        return redirect(url_for('books'))
    return render_template("add_book.html", form = form)


@app.route("/books")
def books():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT id, title, author, category, publication_date, num_pages, available_quantity FROM books")
    books = cur.fetchall()

    if result > 0:
        return render_template("books.html", books = books)
    else:
        msg = "Khong co cuon sach nao"
        return render_template("books.html", msg = msg)
    
    cur.close()


@app.route("/book/<string:id>")
def viewBook(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE id =%s", [id])
    book = cur.fetchone()
    if result > 0:
        return render_template("view_book_details.html", book=book)
    else:
        msg = 'This Book Does Not Exist'
        return render_template("view_book_details.html", warning = msg)
    cur.close()


@app.route("/edit_book/<string:id>", methods = ["GET", "POST"])
def edit_book(id):
    form = AddBook(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE id=%s", [id])
    book = cur.fetchone()
    if request.method == "POST" and form.validate():
        if(form.id.data != id):
            result = cur.execute(
                "SELECT id FROM books WHERE id=%s", [form.id.data]
            )
            book = cur.fetchone()
            if(book):
                error = "Book with that ID already exists"
                return render_template('edit_book.html', form=form, error=error, book=form.data)

        cur.execute("UPDATE books SET id=%s, title=%s, author=%s, category=%s, publication_date=%s, num_pages=%s, available_quantity=%s WHERE id=%s", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.category.data,
            form.publication_date.data,
            form.num_pages.data,
            form.available_quantity.data,
            id])
        mysql.connection.commit()

        cur.close()

        # flash("Book Updated", "SuccesS")
        return redirect(url_for("books"))
    return render_template("edit_book.html", form=form, book=book)


@app.route("/delete_book/<string:id>", methods = ["POST"])
def delete_book(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM books WHERE id=%s", [id])      
        mysql.connection.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        flash("Book could not be deleted", "danger")
        flash(str(e), "danger")
        return redirect(url_for("books"))
    finally:
        cur.close()
    flash("Book Deleted", "success")
    return redirect(url_for("books"))


@app.route("/", methods=["GET", "POST"])
def layout():
    return render_template("layout.html")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = signUpForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]
        password = request.form["password"]
        role = request.form["role"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM account")
        users = str(cur.fetchall())
        cur.execute("SELECT email FROM account")
        mails = str(cur.fetchall())
        if not userName in users and not email in mails:
            if userName.isascii():
                cur.execute("INSERT INTO account (username,password,email,phonenumber,role) VALUES (%s, %s, %s, %s, %s)", [
                userName,
                password,
                email,
                phonenumber,
                role
            ])
                mysql.connection.commit()
                session["userName"] = userName
                flash(f"Welcome {userName}", "success")
                return redirect(url_for("login", direct='&'))
        elif userName in users and email in mails:
            flash("This username and email is unavailable.", "error")
        elif not userName in users and email in mails:
            flash("This email is unavailable.", "error")
        elif userName in users and not email in mails:
            flash("This username is unavailable.", "error")
    return render_template("signup.html", form=form, hideSignup = True)



@app.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            return redirect(direct)
        case False:
            form = loginForm(request.form)
            if request.method == "POST":
                userName = request.form["userName"]
                password = request.form["password"]
                userName = userName.replace(" ", "")
                password = password.replace(" ", "")
                cur = mysql.connection.cursor()
                cur.execute("SELECT username, password, role FROM account WHERE lower(userName) = %s", (userName.lower(),))
                user = cur.fetchone()
                if not user:
                    flash("Tài khoản không tồn tại", "error")
                else:
                    if password.lower() == user["password"]:

                        session["userName"] = user["username"]
                        role_user = user["role"]
                        if role_user.lower() == "admin":
                            flash(f"Welcome admin", "success")
                            return redirect(url_for("admin_home"))
                        elif role_user.lower() == "user":
                            flash(f"Welcome user", "success")
                            return redirect(url_for("layout"))
                    else:
                        flash("Sai mat khau", "error")
    return render_template("login.html", form=form, hideLogin=True)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    match "userName" in session:
        case True:
            session.clear()
            return redirect("/")
        case False:
            return redirect("/")
    return redirect(url_for("login", direct='&'))


@app.route("/index")
def index():
    return render_template("index.html")
# @app.route("/index", methods=["GET"])
# def navbar():
#     return render_template("navbar.html")

if __name__ == "__main__":
    app.secret_key = "secret"
    app.run(debug=True)
    
