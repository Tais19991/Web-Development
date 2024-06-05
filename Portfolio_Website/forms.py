from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField


# Create a form to add new data in portfolio
class CreateDataForm(FlaskForm):
    title = StringField("Data Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle")
    img_main = FileField("Main image (for dataset on index page)", validators=[DataRequired()])
    description = CKEditorField("Data Description", validators=[DataRequired()])
    submit = SubmitField("Submit Data")


# Create a form to login admins
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form to contact me trough Telegram
class ContactFormTG(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(message='Email is required.'),
                                                  Email(message='Invalid email address.', granular_message=False, check_deliverability=False, allow_smtputf8=True, allow_empty_local=False)])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
