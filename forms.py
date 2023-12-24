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
    title = StringField('Tiêu đề', [validators.Length(min=2, max=255)])
    author = StringField('Tác giả', [validators.Length(min=2, max=255)])
    category = StringField('Thể loại', [validators.Length(min=2, max=255)])
    num_pages = IntegerField('Số trang', [validators.NumberRange(min=1)])
    publication_date = DateField(
        'Ngày xuất bản', [validators.InputRequired()])
    available_quantity = IntegerField(
        'Số lượng', [validators.NumberRange(min=1)])
    image = FileField('Anhr', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class BorrowBook(FlaskForm):
    user_id = StringField('User ID', [validators.Length(min=1, max=11)])
    book_id = StringField('Book ID', [validators.Length(min=1, max=11)])
    borrow_date = DateField(
        'Ngày mượn ', [validators.InputRequired()])
    due_date = DateField(
        'Hạn trả', [validators.InputRequired()])
   
 

class BorrowSubmitForm(FlaskForm):
    borrowing_id = StringField('Borrowing ID', [validators.Length(min=1, max=11)])
    title = StringField('Tiêu đề', [validators.Length(min=2, max=255)])
    username = StringField(
        "Tên người dùng",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    borrow_date = DateField(
        'Ngày mượn', [validators.InputRequired()])
    due_date = DateField(
        'Hạn trả', [validators.InputRequired()])
    return_date = DateField(
        'Ngày trả', [validators.InputRequired()])
    

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
