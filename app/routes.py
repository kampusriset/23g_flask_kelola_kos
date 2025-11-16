# MyKost Project
# MIT License (c) 2025 AnakKost Team

from flask import Blueprint, redirect, url_for, render_template # pyright: ignore[reportMissingImports]

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.login'))
