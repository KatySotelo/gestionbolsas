# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:56:43 2025

@author: Katy
"""
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-supersecreta")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Usuario único definido manualmente
USUARIO_VALIDO = {
    "username": "Katy",
    "password": "Katysotelo1"  # Puedes cambiarlo
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USUARIO_VALIDO["username"] and password == USUARIO_VALIDO["password"]:
            user = User(username)
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/ingreso")
@login_required
def ingreso():
    return render_template("ingreso.html")

@app.route("/rebaja")
@login_required
def rebaja():
    return render_template("rebaja.html")


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return User(user_id)
    return None

# Inicializa base de datos
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cajas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref TEXT NOT NULL,
            lot TEXT NOT NULL,
            vencimiento TEXT,
            tipo TEXT,
            cantidad INTEGER,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ingreso', methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':
        ref = request.form['ref']
        lot = request.form['lot']
        vencimiento = request.form['vencimiento']
        tipo = request.form['tipo']
        cantidad = request.form['cantidad']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cajas (ref, lot, vencimiento, tipo, cantidad)
            VALUES (?, ?, ?, ?, ?)
        ''', (ref, lot, vencimiento, tipo, cantidad))
        conn.commit()
        conn.close()
        return redirect('/ingreso')
    
    return render_template('ingreso.html')

@app.route('/rebaja')
def rebaja():
    return render_template('rebaja.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


