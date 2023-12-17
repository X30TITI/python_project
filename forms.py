from wtforms import validators, Form, StringField, PasswordField, TextAreaField
from wtforms import StringField, FloatField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

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

class AddBook(FlaskForm):
    id = StringField('Book ID', [validators.Length(min=1, max=11)])
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])
    category = StringField('Category', [validators.Length(min=2, max=255)])
    num_pages = IntegerField('No. of Pages', [validators.NumberRange(min=1)])
    publication_date = DateField(
        'Publication Date', [validators.InputRequired()])
    available_quantity = IntegerField(
        'Total No. of Books', [validators.NumberRange(min=1)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class BorrowBook(FlaskForm):
    user_id = StringField('User ID', [validators.Length(min=1, max=11)])
    book_id = StringField('Book ID', [validators.Length(min=1, max=11)])
    borrow_date = DateField(
        'Borrow Date', [validators.InputRequired()])
    due_date = DateField(
        'Due Date', [validators.InputRequired()])
   
 

class BorrowSubmitForm(FlaskForm):
    borrowing_id = StringField('Borrowing ID', [validators.Length(min=1, max=11)])
    title = StringField('Title', [validators.Length(min=2, max=255)])
    username = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    borrow_date = DateField(
        'Borrow Date', [validators.InputRequired()])
    due_date = DateField(
        'Due Date', [validators.InputRequired()])
    return_date = DateField(
        'Return Date', [validators.InputRequired()])
    

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
    password = StringField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "password"},
    )
    phonenumber = StringField("Phonenumber",[
            validators.Length(max=9),
            validators.InputRequired()],
            render_kw={"placeholder": "phonenumber"},
            )
    
    role = StringField(
        "Role",
        [
            validators.Length(min=4),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "role"},
    )
