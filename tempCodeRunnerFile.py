from flask import Flask, flash,render_template, request, redirect, url_for, session, send_from_directory
from forms import loginForm, AddBook, signUpForm, BorrowBook, BorrowSubmitForm
# from flask_uploads import UploadSet, IMAGES, configure_uploads
import MySQLdb
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.secret_key = "secret"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'LibraryDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['UPLOAD_PATH'] = "C:\\Users\\ACER\\Desktop\\BT_Python\\app\\static"

@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    form = AddBook()
    if request.method == "POST" and form.validate():
        upload_image = form.image.data
        filenames = secure_filename(upload_image.filename)
        image_path = os.path.join(app.config['UPLOAD_PATH'], filenames)
        upload_image.save(image_path)
        print(upload_image.filename)
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT id FROM books WHERE id=%s", [form.id.data])
        book = cur.fetchone()
        if(book):
            error = "Id da ton tai"
            return render_template('add_book.html', form=form, error=error)
        cur.execute("INSERT INTO books (id,title,author,category,publication_date,num_pages,available_quantity,image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.category.data,
            form.publication_date.data,
            form.num_pages.data,
            form.available_quantity.data,
            upload_image.filename
        ])
        mysql.connection.commit()
        cur.close()
        flash("New Book Added", "success")
        # Redirect to show all books
        return redirect(url_for('books'))
    return render_template("add_book.html", form = form)


@app.route("/books")
def books():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT id, title, author, category, publication_date, num_pages, available_quantity, image_path FROM books")
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
    form = AddBook()
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE id=%s", [id])
    book = cur.fetchone()
    if request.method == "POST" and form.validate():
        upload_image = form.image.data
        filenames = secure_filename(upload_image.filename)
        image_path = os.path.join(app.config['UPLOAD_PATH'], filenames)
        upload_image.save(image_path)
        print(upload_image.filename)
        if(form.id.data != id):
            result = cur.execute(
                "SELECT id FROM books WHERE id=%s", [form.id.data]
            )
            book = cur.fetchone()
            if(book):
                error = "Book with that ID already exists"
                return render_template('edit_book.html', form=form, error=error, book=form.data)
        cur.execute("UPDATE books SET id=%s, title=%s, author=%s, category=%s, publication_date=%s, num_pages=%s, available_quantity=%s, image_path=%s WHERE id=%s", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.category.data,
            form.publication_date.data,
            form.num_pages.data,
            form.available_quantity.data,
            upload_image.filename,
            id])
        mysql.connection.commit()
        cur.close()
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

@app.route("/borrow_book/<string:id>",  methods = ["GET", "POST"])
def borrow_book(id):
    form = BorrowBook()
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE id=%s", [id])
    book = cur.fetchone()
    if request.method == "POST" and form.validate():
      
        cur.execute("INSERT INTO transactions(user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)", [
                form.user_id.data,
                form.book_id.data,
                form.borrow_date.data,
                form.due_date.data
        ])
        mysql.connection.commit()
        cur.close()
        flash("Borrow book", "success")
        return redirect(url_for("user"))
    return render_template("borrow_book.html", form=form, book=book)

@app.route("/borrow_list", methods = ["GET", "POST"])
def borrow_list():
    cur = mysql.connection.cursor()
    result = cur.execute("""SELECT borrowing_id, title, username,borrow_date, due_date, return_date 
                        FROM books b INNER JOIN transactions t ON b.id = t.book_id 
                        INNER JOIN account a ON t.user_id = a.id 
                        where return_date is null""")
    
    historys = cur.fetchall()
    if result > 0:
        return render_template("admin_borrow_list.html", historys = historys)
    else:
        msg = "Khong co cuon sach nao"
        return render_template("admin_borrow_list.html", msg = msg)
    cur.close()

@app.route("/borrow_submit/<string:id>", methods = ["GET", "POST"])
def borrow_submit(id):
    form = BorrowSubmitForm()
    cur = mysql.connection.cursor()
    result = cur.execute("""SELECT borrowing_id, title, username,borrow_date, due_date, return_date
                        FROM books b INNER JOIN transactions t ON b.id = t.book_id 
                        INNER JOIN account a ON t.user_id = a.id 
                        where return_date is null and borrowing_id=%s""", [id])
    history = cur.fetchone()
    print(history["borrowing_id"])
    if request.method == "POST" and form.validate():
        cur.execute("UPDATE transactions SET return_date=%s WHERE borrowing_id=%s", [
            form.return_date.data,
            id])
        mysql.connection.commit()
        cur.close()
        flash("Xac nhan", "success")
        return redirect(url_for('borrow_list'))
    return render_template("admin_borrow_submit.html", form=form, history=history)

@app.route("/history_borrow", methods = ["GET", "POST"])
def history_borrow():
    user_info = session.get("userName")
    print(user_info)
    cur = mysql.connection.cursor()
    result = cur.execute("""SELECT book_id, title, username,borrow_date, due_date, return_date
                            FROM books b INNER JOIN transactions t ON b.id = t.book_id 
                            INNER JOIN account a ON t.user_id = a.id 
                            where return_date is not null and username=%s""", [user_info])
    historys = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("history_borrow_user.html", historys=historys)


@app.route("/user_info", methods=["GET", "POST"])
def user_info():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM account WHERE role = 'user'")
    users = cur.fetchall()
    if result > 0:
        return render_template("user_info.html", users=users)
    else:
        msg = 'Khong co user'
        return render_template("user_info.html", warning = msg)
    cur.close()


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
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
        elif userName in users and email in mails:
            flash("This username and email is unavailable.", "error")
        elif not userName in users and email in mails:
            flash("This email is unavailable.", "error")
        elif userName in users and not email in mails:
            flash("This username is unavailable.", "error")
        return redirect(url_for('user_info'))
    return render_template("add_user.html", form=form)


@app.route("/edit_user/<string:id>", methods=["GET", "POST"])
def edit_user(id):
    form = signUpForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM account WHERE id=%s", [id])
    user = cur.fetchone()
    if request.method == "POST" and form.validate():
        cur.execute("UPDATE account SET username=%s, password=%s, email=%s, phonenumber=%s, role=%s WHERE id=%s", [
            form.userName.data,
            form.password.data,
            form.email.data,
            form.phonenumber.data,
            form.role.data,
            id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("user_info"))
    return render_template("edit_user.html", form=form, user=user)


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
                            return redirect(url_for("user"))
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


@app.route("/user")
def user():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT id, title, author, category, publication_date, num_pages, available_quantity, image_path FROM books")
    books = cur.fetchall()

    if result > 0:
        return render_template("user.html", books = books)
    else:
        msg = "Khong co cuon sach nao"
        return render_template("books.html", msg = msg)
    cur.close()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == "__main__":
    app.run(debug=True)