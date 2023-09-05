from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from flask_wtf import FlaskForm
from flask_login import LoginManager

login_manager = LoginManager()


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField('Confirm password', validators=[Length(min=8), EqualTo(password1), DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15)])
    email = EmailField('Email', validators=[Email()])
    first_name = StringField('First Name', validators=[Length(min=0, max=50)])
    last_name = StringField('Last Name', validators=[Length(min=0, max=50)])
    phone_number = StringField('Phone Number', validators=[Length(min=8, max=8), Regexp(regex='^[+-]?[0-9]$')])
    address = StringField('Address')
    credit_number = StringField('Credit Card Number', validators=[Length(min=16, max=16), Regexp(regex='^[+-]?[0-9]$')])
    credit_cvv = StringField('CVV', validators=[Length(min=3, max=3), Regexp(regex='^[+-]?[0-9]$')])
    credit_date = DateField('Date of Expiry')
    profile_picture = FileField('Profile Picture')
    submit = SubmitField('Save Changes')


class ChangePasswordForm(FlaskForm):
    password = StringField('Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField('Save Changes')

class CreateCreditCardForm(FlaskForm):
    card_name = StringField('Name on Card', validators=[Length(min=0, max=50), DataRequired()])
    credit_number = StringField('Credit Card Number', validators=[Length(min=16, max=16), Regexp(regex='^[+-]?[0-9]$'), DataRequired()])
    credit_cvv = StringField('CVV', validators=[Length(min=3, max=3), Regexp(regex='^[+-]?[0-9]$'), DataRequired()])
    expiry_date = DateField('Date of Expiry',validators=[DataRequired()])
    submit = SubmitField('Add Card')
