from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, widgets
from wtforms.validators import InputRequired, Email

class NewsletterForm(FlaskForm):
    email = StringField("email", widget=widgets.Input(input_type="email"),
                        render_kw=dict(class_="form-control", placeholder="Enter your email"),
                        validators=[InputRequired(), Email()])

class SearchForm(FlaskForm):
    search = StringField("search", render_kw=dict(class_="form-control", placeholder="Search..."),
                        validators=[InputRequired()])

class ContactForm(FlaskForm):
    first_name = StringField("First Name", render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired()])
    last_name = StringField("Last Name", render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired()])
    email = StringField("Email Address", widget=widgets.Input(input_type="email"),
                        render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired(), Email()])
    tel_number = IntegerField("Tel. Number", render_kw=dict(class_ = "form-control form-control-lg"),
                              widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    message = TextAreaField("Message", render_kw=dict(class_ = "form-control", cols="30", rows="10"), validators=[InputRequired()])
    submit = SubmitField("Send Message", render_kw=dict(class_ = "btn btn-primary py-3 px-5"))