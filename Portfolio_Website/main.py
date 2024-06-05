import requests
import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import check_password_hash
from forms import CreateDataForm, LoginForm, ContactFormTG
import logging

logging.basicConfig(level=logging.DEBUG)


UPLOAD_FOLDER = 'static/assets/img'


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_S_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
Bootstrap5(app)

# ----------------------------------------Configure Flask-Login------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(admin_id):
    return db.get_or_404(Admin, admin_id)


# ---------------------------------------------- DATABASE--------------------------------------------
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# --------------------------------------------CONFIGURE TABLES-----------------------------------------
class PortfolioSet(db.Model):
    __tablename__ = "portfolio_sets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    img_main: Mapped[str] = mapped_column(String(250), nullable=False)


# Create an Admin table for all registered Admins
class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()


# ----------------------------------------SET ADMIN FUNC---------------------------------------------
# An admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(Admin).where(Admin.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('admin_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('admin_login'))
        else:
            login_user(user)
            return redirect(url_for('index'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/new-data", methods=["GET", "POST"])
@admin_only
def add_new_data():
    form = CreateDataForm()
    if form.validate_on_submit():
        new_data = PortfolioSet(
            title=form.title.data,
            subtitle=form.subtitle.data,
            description=form.description.data,
            img_main=form.img_main.data.filename)
        # save img in project folder
        form.img_main.data.save(os.path.join(app.config['UPLOAD_FOLDER'], form.img_main.data.filename))
        # add data to db
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_data.html", form=form)


@app.route("/edit-post/<int:data_id>", methods=["GET", "POST"])
@admin_only
def edit_data(data_id):
    data = db.get_or_404(PortfolioSet, data_id)
    data_to_edit = CreateDataForm(
        title=data.title,
        subtitle=data.subtitle,
        img_main=data.img_main,
        description=data.description,
    )

    if data_to_edit.validate_on_submit():
        data.title = data_to_edit.title.data
        data.subtitle = data_to_edit.subtitle.data
        data.img_main = data_to_edit.img_main.data.filename
        data.description = data_to_edit.description.data
        # save img in project folder
        data_to_edit.img_main.data.save(os.path.join(app.config['UPLOAD_FOLDER'], data.img_main))
        db.session.commit()

        return redirect(url_for("index", data_id=data.id))
    return render_template("add_data.html", form=data_to_edit, is_edit=True)


@app.route("/delete/<int:data_id>")
@admin_only
def delete_data(data_id):
    data_to_delete = db.get_or_404(PortfolioSet, data_id)
    db.session.delete(data_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/logout')
@admin_only
def logout():
    logout_user()
    return redirect(url_for('index'))


# --------------------------------------------OPEN PAGES--------------------------------------------

@app.route("/")
def index():
    result = db.session.execute(db.select(PortfolioSet))
    data = result.scalars().all()
    return render_template("index.html", portfolio_data=data, current_user=current_user)


TELEGRAM_TOKEN = os.environ.get("TG_TOKEN")
TELEGRAM_ID = os.environ.get("TG_ID")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form_tg = ContactFormTG()
    if request.method == "POST":
        send_tg_msg(form_tg.name.data, form_tg.email.data, form_tg.message.data)
        flash('Your message has been successfully sent', 'info')
        return render_template('contact.html', form=form_tg, is_sent=True)

    return render_template("contact.html", form=form_tg)


def send_tg_msg(name, phone, message):
    message_to_send = f"From: {name},\n Phone: {phone},\n Message: {message}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_ID}&text={message_to_send}"
    requests.get(url).json()


if __name__ == "__main__":
    app.run(debug=True)
