from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def.main():
    return render_template('lab7/index.html')