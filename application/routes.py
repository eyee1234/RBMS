from application import app,db
from flask import render_template,request,json,Response,redirect,flash

from application.models import User,Course,Enrollment
from application.forms import LoginForm,RegisterForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",login=True)

@app.route("/login",methods=['GET','POST'])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     email       = form.email.data
    #     password    = form.password.data


    #     user=User.objects(email=email).first()
    #     if user and password == user.password:
    #         flash(f"{user.first_name},You are successfully logged in!","success")
    #         return redirect("/index")
    #     else:
    #         flash("Invalid username password","danger")
    # return render_template("login.html",title="Login",form=form , login=True)
    return render_template("login.html",title="Login",login=True)        

@app.route("/register")
def register():
    return render_template("register.html")



    
