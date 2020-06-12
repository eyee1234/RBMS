from application import app,db
from flask import render_template,request,json,Response,redirect,flash,session,url_for

from application.models import User
from application.forms import LoginForm,RegisterForm

import time
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



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
            session['userId'] = user.userId
            session['roleId'] = user.roleId
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
    session['userId']=False
    session['roleId']=False
    session['username']=None
    return redirect(url_for('index'))

def obj_dict(data):
    return data.__dict__
@app.route("/getrole")
def getrole():
    if session.get('userId'):
        data=list(User.objects.only(*['email']).aggregate(*[
                {
                    '$match': {
                        'userId': session.get('userId')
                    }
                }, {
                    '$lookup': {
                        'from': 'role', 
                        'localField': session.get('roleId'), 
                        'foreignField': session.get('roleId'), 
                        'as': 'role'
                    }
                }, {
                    '$unwind': {
                        'path': '$role', 
                        'preserveNullAndEmptyArrays': False
                    }
                }
            ]))[0]
        print(data)
        print(data['role']['name'])
        # results=[]
        # for document in data:
        #     document['_id'] = str(document['_id'])
        #     results.append(document)
        # print("results:",results)
        # json.encode(data, cls=JSONEncoder)
        # data=JSONEncoder().encode(data)
        # json_string = json.dumps(data, default=obj_dict)

        # return json.dumps(json_string)
    return redirect("/login")