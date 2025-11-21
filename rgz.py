from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from os import path

rgz = Blueprint('rgz', __name__)