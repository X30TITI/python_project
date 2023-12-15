
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