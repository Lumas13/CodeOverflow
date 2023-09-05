from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, FileField
from wtforms.fields import EmailField, DateField
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf import FlaskForm
from flask_login import LoginManager
from wtforms import FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class CreateInventoryForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_desc = StringField('Product Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    category = SelectField('Category',[validators.DataRequired()], default=(0, "fruits"), choices=[(0, "fruits"), (1, "vegetables"), (2, "drinks")])
    price = StringField('Price', [validators.DataRequired()], default='1')
    discount = StringField('Discount', default='0')
    quantity = StringField('Quantity', [validators.DataRequired()], default='1')
    product_image = FileField('Image of product:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class CreateSalesForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    quantity_bought = StringField('Quantity', default='0')

class CreateCustomerForm(Form):
    customer_name = StringField('Customer Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    contact_number = StringField('Contact Number', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    shipping_address = StringField('Shipping Address', [validators.DataRequired()])
    card_no = StringField('Card Number', [validators.DataRequired()])

class CreateFeedbackForm(Form):
    name = StringField('Your Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Your Email', [validators.Email(), validators.DataRequired()])
    question1 = TextAreaField('How do you feel about the website?', [validators.DataRequired()])
    question2 = TextAreaField('What did you like about the website?', [validators.DataRequired()])
    question3 = TextAreaField('What improvements to the website do you think we can make?', [validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.DataRequired()])

class CreateReportForm(Form):
    name = StringField('Your Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Your Email', [validators.Email(), validators.DataRequired()])
    contact = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    problem = SelectField('Select Problem', [validators.DataRequired()], choices=[('', 'Select Problem'), ('M', 'Missing Item'), ('D', 'Damaged Item'), ('C', 'Cancel Order'), ('O','Others')], default='')
    other = TextAreaField('If the above selected "Others". If not applicable please input NIL', [validators.DataRequired()])
    date = DateField('Date When Problem Occurred', [validators.DataRequired()])
    report_image = FileField('Image of product:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    remarks = TextAreaField('Describe The Problem Faced', [validators.DataRequired()])



