from flask import render_template, request, redirect, url_for, flash, session
from . import auth
from ..utils.api import login_user, register_user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, token, error = login_user(username, password)

        if success:
            session["token"] = token
            return redirect(url_for("dashboard.index"))
        else:
            flash(error or "Invalid credentials", "danger")

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Validate input
        if not username or not password or not email:
            flash("All fields are required", "danger")
            return render_template("auth/register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long", "danger")
            return render_template("auth/register.html")

        # Register the user
        success, message = register_user(username, password, email)

        if success:
            # If registration successful, automatically log the user in
            login_success, token, login_error = login_user(username, password)

            if login_success:
                session["token"] = token
                flash("Account created successfully!", "success")
                return redirect(url_for("dashboard.index"))
            else:
                # Fall back to manual login if auto-login fails
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("auth.login"))
        else:
            flash(f"Registration failed: {message}", "danger")

    return render_template("auth/register.html")


@auth.route("/logout")
def logout():
    session.pop("token", None)
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))
