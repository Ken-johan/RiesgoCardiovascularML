from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

if __name__ == '_main_':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entendimiento-negocio')
def entendimiento_negocio():
    return render_template('entendimiento_negocio.html')

@app.route('/entendimiento-datos')
def entendimiento_datos():
    return render_template('entendimiento_datos.html')

@app.route('/ingenieria-datos')
def ingenieria_datos():
    return render_template('ingenieria_datos.html')

@app.route('/ingresar')
def ingresar():
    return render_template('ingresar.html')

