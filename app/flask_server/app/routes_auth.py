# library -> flask
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    render_template,
    session,
    jsonify,
    send_file,
    flash,
)

# library -> protect routes from no-authorized acces by wrapper
from flask_login import fresh_login_required, login_required, login_user, logout_user

# library -> manage (hashed) password
from werkzeug.security import check_password_hash, generate_password_hash

# script -> import Flask forms
from .forms import LoginForm, RegistrationForm, SearchForm, SearchPatientForm

# sciprt -> manage acces to different layers of app (admin mode / no-admin mode)
from .role_req import admin_required

# script -> database model patient database and user database (ibm db2 / sqlite)
from .models import User, Patient

# sciprt -> add protection during loging to app
from .safe_url import is_safe_url

# __init__ -> import sqlachemy
from . import db

# libarary -> generate tokenk by standard python libarary for Universally Unique Identifier
import uuid

# library -> encode blop file(image) from patient database(db2 database)
from base64 import b64encode

# script -> store variables in back-end
from .store_tmp import StoreID, StoreIP, Counter

# library -> create pdf from html
import pdfkit

# library -> time / date
import datetime

import time

from flask import session, g

# set 2. blueprint = auth
auth = Blueprint("auth", __name__)


# redirect page -> index route:
# Note:
#   1. This route is acces point route which redirect to sign in page
@auth.route("/")
def index():
    return redirect(url_for(".sign_in"))


# page -> route sign in:
# Note:
#   1. This route manage acces to database,
#   2. import login form
#       * input: email and password
#   3. find user by inputed email if exist
#   4. check if passwords match
#   5. create user session for manage cookie acces
#   6. if is next url safe, redirect to home page depend on role mode
@auth.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):

                user.session_token = str(uuid.uuid4())
                db.session.commit()

                login_user(user, remember=False)

                if "next" in session:
                    next = session["next"]

                    if is_safe_url(next) and next is not None:
                        return redirect(next)

                if user.role == "Admin":
                    flash("admin sign in")
                    return redirect(url_for(".home_admin"))

                else:
                    flash("user sign in")
                    return redirect(url_for("app.home"))

        return render_template("sign_in.html", form=form, wrong=True)

    session["next"] = request.args.get("next")
    return render_template("sign_in.html", form=form, wrong=False)


# page -> admin level -> route home:
# Note:
#   1. All users are filtred and add to main table.
#   2. Create search form for fast finding users.
#       * if is hit search button, find in database by defined inputs.
#       *   inputs: surname - email - session token
#       *   return searched users
@auth.route("/home_admin", methods=["GET", "POST"])
@admin_required
@login_required
def home_admin():
    users = User.query.filter().all()

    db.session.flush()

    search_form = SearchForm()

    if search_form.validate_on_submit() and search_form.search.data:
        search_user = User.query.filter(
            (User.surname == search_form.surname.data)
            | (User.email == search_form.email.data)
            | (User.session_token == search_form.session_token.data)
        ).all()
        return render_template(
            "admin/home_admin.html",
            users=users,
            search_list=search_user,
            search_form=search_form,
        )

    return render_template(
        "admin/home_admin.html", users=users, search_form=search_form
    )


# page -> admin level -> route documentation camera:
# Note:
#   1. Documentation page -> camera datasheet
@auth.route("/documentation_cam")
@admin_required
@login_required
def documentation_cam():
    return render_template("admin/documentation_cam.html")


# page -> admin level -> route documentation robot:
# Note:
#   1. Documentation page -> robot datasheet
@auth.route("/documentation_robot")
@admin_required
@login_required
def documentation_robot():
    return render_template("admin/documentation_robot.html")


# ajax -> admin level -> route admin changes:
# Note:
#   1. get user by ajax call, find in database and by posted data, change or delete.
#   2. approach -> if is post all user data -> change it
#   3. approach -> if is post data short -> delete it
@auth.route("/change_admin", methods=["GET", "POST"])
@admin_required
@login_required
def change_admin():
    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(id=data[0]).first()

        if len(data) == 1:
            db.session.delete(user)

            db.session.commit()

            return jsonify({"allert": "User was succesfully delete!"})

        else:
            user.email = data[1]
            user.role = data[2]
            user.title = data[3]
            user.username = data[4]
            user.surname = data[5]
            user.department = data[6]

            db.session.commit()

            return jsonify({"allert": "Data was succesfully changed!"})

    return redirect(url_for(".home_admin"))


# page -> admin level -> route admin register:
# Note:
#   1. registration form, then if is hit submit button check data and then,
#   commit to database of users (sqlite)
@auth.route("/register_admin", methods=["GET", "POST"])
@admin_required
@login_required
def register_admin():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit() and reg_form.register.data:
        # generate password by SHA256
        user = User(
            username=reg_form.username.data,
            surname=reg_form.surname.data,
            email=reg_form.email.data,
            password=generate_password_hash(reg_form.password.data),
            title=reg_form.title.data,
            role=reg_form.role.data,
            department=reg_form.role.data,
        )

        db.session.add(user)
        db.session.commit()

        # this is necessary for reloading page
        return redirect(url_for(".register_admin"))

    return render_template("admin/register_admin.html", reg_form=reg_form)


# page -> route patient find:
# Note:
#   1. search patient form
#       * only 1. input
@auth.route("/patient_find", methods=["GET", "POST"])
@login_required
def patient_find():
    search_form = SearchPatientForm()
    return render_template("patient_find.html", search_form=search_form)


# page -> route patient searched:
# Note:
#   1. from route patient find get data, and filter all patient by given input.
#       * inputs by which the database is searched is only: patient surname or Personal Identification Number
#   2. If is not finded patient then just render page -> jinja detect no data -> warning no patient find
@auth.route("/patients_searched", methods=["GET", "POST"])
@login_required
def patients_searched():
    find = request.form.get("search_data")
    patients = (
        Patient.query.with_entities(
            Patient.name, Patient.surname, Patient.dob, Patient.pid
        )
        .filter((Patient.pid == find) | (Patient.surname == find))
        .all()
    )

    if patients:
        return render_template("patients_searched.html", patients=patients)

    else:
        return render_template("patients_searched.html")

    return render_template("patients_searched.html")


# function -> route patient generate:
# Note:
#   1. create automatically html page by given data of initialized patient
#   2. create patient declaration
@auth.route("/patient_gen")
def patient_gen():
    if StoreID.id == 0:
        return render_template("404.html")

    else:
        time = datetime.datetime.now()
        patient = Patient.query.filter_by(pid=StoreID.id).first()
        image = b64encode(patient.photo).decode("utf-8")
        return render_template(
            "/gen_pdf/template.html",
            patient=patient,
            obj=patient.photo,
            image=image,
            time=time,
        )


# function -> route download:
# Note:
#   1. find route patient gen
#   2. create from html page pdf
#   3. download on client side
@auth.route("/download")
@login_required
def download():
    pdfkit.from_url(request.host + "/patient_gen", "app/pdf/patient_declaration.pdf")
    path = "pdf/patient_declaration.pdf"
    try:
        return send_file(path, as_attachment=True)

    except FileNotFoundError:
        return render_template("404.html")


# page -> route patient data:
# Note:
#   1. show all data from db2 ibm database of patient
#   2. get all numbers / strings / blob file -> decoded by b64
#   2. init patient
@auth.route("/patient_data", methods=["GET", "POST"])
@login_required
def patient_data():
    find = request.form["patient"]
    patient = Patient.query.filter_by(pid=find).first()
    image = b64encode(patient.photo).decode("utf-8")

    StoreID.id = find

    return render_template(
        "patient_data.html", patient=patient, obj=patient.photo, image=image
    )


# !!redirect page -> route sign out:
# Note:
#   1. all back end variables init to originals values and disconnect all devices
#   2. in progress
@auth.route("/sign_out")
@login_required
def sign_out():
    # TODO delete all cookies!!
    StoreIP.ip = "none"
    StoreID.id = 0
    Counter.counter = 0
    logout_user()
    return redirect(url_for(".sign_in"))


@auth.teardown_request
def teardown_request_func(error=None):
    if error:
        # Log the error
        print(str(error))


@auth.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404
