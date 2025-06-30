# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:56:43 2025

@author: Katy
"""
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

