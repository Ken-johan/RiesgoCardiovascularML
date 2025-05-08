from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random


app = Flask(__name__)

if __name__ == '_main_':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ingresar')
def Ingresar():
    return render_template('ingresar.html')