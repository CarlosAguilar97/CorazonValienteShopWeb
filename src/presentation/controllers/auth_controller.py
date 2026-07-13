from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.application.use_cases.auth.login_user import LoginUserUseCase


def login_get():
    return render_template("admin/login.html")


def login_post():
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    use_case = LoginUserUseCase()
    user = use_case.execute(email, password)

    if not user:
        flash("Credenciales incorrectas.", "error")
        return render_template("admin/login.html"), 401

    login_user(user, remember=True)
    return redirect(url_for("admin.dashboard"))


def logout():
    logout_user()
    return redirect(url_for("auth.login"))
