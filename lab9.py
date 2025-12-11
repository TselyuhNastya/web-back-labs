from flask import Blueprint, render_template, jsonify, request, session

lab9 = Blueprint('lab9', __name__)

congratulations = [
    "С Новым годом! Пусть сбываются мечты!",
    "Желаю здоровья, счастья и удачи!",
    "Пусть новый год принесёт много радости!",
    "Успехов в работе и учёбе!",
    "Мира, добра и благополучия!",
    "Исполнения всех желаний!",
    "Крепких семейных уз!",
    "Финансового процветания!",
    "Интересных путешествий!",
    "Творческих успехов!"
]

box_images = [f"/static/lab9/box{i+1}.png" for i in range(10)]
gift_images = [f"/static/lab9/gift{i+1}.jpg" for i in range(10)]

POSITIONS = [
    (15, 10), (25, 30), (40, 15), (60, 25), (20, 50),
    (35, 65), (55, 45), (70, 35), (45, 75), (65, 80)
]

def init_boxes():
    return [{
        'id': i,
        'top': POSITIONS[i][0],
        'left': POSITIONS[i][1],
        'opened': False,
        'congratulation': congratulations[i],
        'box_image': box_images[i],
        'gift_image': gift_images[i]
    } for i in range(10)]

@lab9.route('/lab9/')
def main():
    if 'boxes' not in session:
        session['boxes'] = init_boxes()
        session['opened_count'] = 0
    return render_template('lab9/index.html')

@lab9.route('/lab9/api/open_box', methods=['POST'])
def open_box():
    box_id = request.json.get('box_id')
    
    if 'boxes' not in session:
        return jsonify({'error': 'Сессия не инициализирована'}), 400
    
    boxes = session['boxes']
    if box_id < 0 or box_id >= len(boxes):
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    box = boxes[box_id]
    if box['opened']:
        return jsonify({'error': 'Эта коробка уже открыта'}), 400
    
    if session['opened_count'] >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество коробок (3)'}), 400
    
    box['opened'] = True
    session['opened_count'] += 1
    session['boxes'] = boxes
    
    remaining = sum(1 for b in boxes if not b['opened'])
    
    return jsonify({
        'success': True,
        'congratulation': box['congratulation'],
        'gift_image': box['gift_image'],
        'box_image': box['box_image'],
        'opened_count': session['opened_count'],
        'remaining': remaining
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset_boxes():
    session['boxes'] = init_boxes()
    session['opened_count'] = 0
    return jsonify({'success': True})

@lab9.route('/lab9/api/status')
def get_status():
    if 'boxes' not in session:
        session['boxes'] = init_boxes()
        session['opened_count'] = 0
    
    boxes = session['boxes']
    remaining = sum(1 for b in boxes if not b['opened'])
    
    return jsonify({
        'opened_count': session['opened_count'],
        'remaining': remaining
    })

@lab9.route('/lab9/api/get_boxes')
def get_boxes():
    if 'boxes' not in session:
        session['boxes'] = init_boxes()
        session['opened_count'] = 0
    
    return jsonify({'boxes': session['boxes']})