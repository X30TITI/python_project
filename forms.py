from wtforms import validators, Form, StringField, PasswordField, TextAreaField
from wtforms import StringField, FloatField, IntegerField, DateField, SelectField


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=8), validators.InputRequired()],
        render_kw={"placeholder": "password"},
    )


class AddBook(Form):
    id = StringField('Book ID', [validators.Length(min=1, max=11)])
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])
    category = StringField('Category', [validators.Length(min=2, max=255)])
    num_pages = IntegerField('No. of Pages', [validators.NumberRange(min=1)])
    publication_date = DateField(
        'Publication Date', [validators.InputRequired()])
    available_quantity = IntegerField(
        'Total No. of Books', [validators.NumberRange(min=1)])


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "password"},
    )
    phonenumber = IntegerField("Phonenumber",[
            validators.Length(min=10),
            validators.InputRequired()],
            render_kw={"placeholder": "phonenumber"},
            )
    
    role = StringField(
        "passwordConfirm",
        [
            validators.Length(min=4),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "role"},
    )
