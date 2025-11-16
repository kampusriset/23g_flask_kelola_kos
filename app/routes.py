# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')

def index():
    return render_template('index.html')