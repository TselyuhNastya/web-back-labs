from flask import Blueprint, url_for, request, render_template, make_response, redirect, session
lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')