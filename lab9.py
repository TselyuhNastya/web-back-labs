from flask import Blueprint, render_template, jsonify, request, session, current_app
import random
import os
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')