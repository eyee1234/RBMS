from application import app,db
from flask import render_template,request,json,Response,redirect,flash,session,url_for

from application.models import User
from application.forms import LoginForm,RegisterForm

@app.route("/")
@app.route("/index")
def index():
    if session.get('username'):
        return render_template("index.html",login=True)
    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm(email="hello@gmail.com",password="123456")
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        print("password:",password)

        user=User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name},You are successfully logged in!","success")
            session['use_id'] = user.userId
            session['username'] = user.first_name
            session['roleId'] = user.roleId 
            return redirect("/index")
        else:
            flash("Invalid username password","danger")
    return render_template("login.html",title="Login",form=form , login=True)


@app.route("/register" , methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form=RegisterForm()
    form.password.value="123456"
    form.email.data="ema"
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name  = form.last_name.data
        role_id = form.role_id.data

        user=User(userId=user_id,email=email,first_name=first_name,last_name=last_name,roleId=role_id)
        user.set_password(password)
        user.save()




        flash("You are registered","success")
        return redirect('/index')
    return render_template("register.html",title="Register",form=form)


@app.route("/logout")
def logout():
    session['user_id']=False
    session['username']=None
    return redirect(url_for('index'))

    
