from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField,\
    SelectField, IntegerField, widgets, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email, Length
from flask_wtf.file import FileRequired, FileAllowed

from mdblog.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", render_kw=dict(placeholder = "Username"), validators=[InputRequired()])
    password = PasswordField("Password", render_kw=dict(placeholder = "Password"), validators=[InputRequired()])
    submit = SubmitField("Login", render_kw=dict(class_ = "button"))

class RegisterForm(FlaskForm):
    username = StringField("Username", render_kw=dict(placeholder = "Username"),
                           validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", render_kw=dict(placeholder = "Password"), validators=[InputRequired()])
    confirm_password = PasswordField("Confirm_password",  render_kw=dict(placeholder = "Confirm password"),
                                      validators=[InputRequired(), EqualTo("password")])
    email = StringField("Email", render_kw=dict(placeholder = "Email"), validators=[InputRequired(), Email()])
    submit = SubmitField("Register", render_kw=dict(class_ = "button"))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", render_kw=dict(placeholder="Old password"), validators=[InputRequired()])
    new_password = PasswordField("New password", render_kw=dict(placeholder="New password"), validators=[InputRequired()])
    submit = SubmitField("Change", render_kw=dict(class_="button"))

class ChangeImageForm(FlaskForm):
    image = FileField("New image", validators=[FileRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Change", render_kw=dict(class_="button"))

class ArticleForm(FlaskForm):
    title = StringField("title", render_kw=dict(placeholder = "Title"), validators=[InputRequired()])
    content = TextAreaField("content", render_kw=dict(placeholder = "Content", cols="30", rows="10"), validators=[InputRequired()])
    reading_time = IntegerField("reading_time", widget=widgets.Input(input_type="number"),
                    render_kw=dict(placeholder = "Reading time"), validators=[InputRequired()])
    category = SelectField("Category", choices=[("Events", "Events"), ("Politics", "Politics"), ("Business", "Business"),
                                                ("Health", "Health"), ("Desing", "Desing"), ("Sport", "Sport")])
    image = FileField("image", validators=[FileRequired()])
    submit = SubmitField("CREATE", render_kw=dict(class_ = "button"))