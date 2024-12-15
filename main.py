from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
import os
import json
from crumple_engine import preprocess_image, extract_text_from_image, extract_items_and_prices, filter_food_items
import uuid

app = Flask(__name__)

# Load food database
with open('format_index.json', 'r') as f:
    FORMAT_INDEX = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM receipts WHERE email=?", ('example@crumple.com',))
    data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    pass

if __name__ == '__main__':
    app.run(debug=True)