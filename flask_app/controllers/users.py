from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user, dojoMember
from flask import render_template, request, redirect, session

bcrypt = Bcrypt(app) # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument

#Routes below

@app.route("/log_reg_page")
def log_reg_page():
    return render_template("log_reg_page.html")

@app.route("/register", methods=["POST"])
def user_registration():
    # Validate the registration first
    if not user.User.validate_registration(request.form):
        return redirect("/log_reg_page")
    # Save the newly registered user to the DB
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "account_type": request.form["account_type"],
    }
    session["user_id"] = user.User.user_registration(data)
    # Redirect them appropriately
    if request.form["account_type"] == "admin":
        return redirect("/member/dashboard")
    else:
        return redirect("/home")

@app.route("/login", methods=["POST"])
def log_user_in():
    # We return the User object or False if the validations are no good
    valid_user = user.User.validate_login(request.form)
    # Validate the registration first
    if not valid_user:
        return redirect("/log_reg_page")
    # Get the correct user's id and save in session
    session["user_id"] = valid_user.id
#     # Redirect them appropriately
# <<<<<<< HEAD
    if valid_user.account_type == "admin":
        return redirect("/member/dashboard")
    else:
        return redirect("/home")

    # return redirect("/member/dashboard")
#     return redirect("/member/dashboard")
# >>>>>>> JRO

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route('/logout')
def log_user_out():
    session.clear()
    return redirect('/')

# route that shows all the member the logged in user has added
@app.route('/member/user/account')
def user_member_page():
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("your_dojoMembers.html",this_user= user.User.get_user_by_id(data), all_member = dojoMember.DojoMember.get_all_member())
