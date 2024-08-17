import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room, emit
from game_manager import GameManager
from flask_mysqldb import MySQL

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
game_manager = GameManager()

app.config['MYSQL_HOST'] = os.getenv('DATABASE_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD', 'yourpassword')
app.config['MYSQL_DB'] = os.getenv('DATABASE_DB', 'wordle_db')

# 로깅 설정 (파일과 콘솔 동시에)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# 로그 파일 핸들러 설정 (일별 회전)
log_file_handler = TimedRotatingFileHandler('logs/app.log', when="midnight", interval=1)
log_file_handler.suffix = "%Y-%m-%d"
log_file_handler.setFormatter(log_formatter)
log_file_handler.setLevel(logging.INFO)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)
logger.addHandler(console_handler)

@app.route('/')
def ping():
    return "pong", 200

# 예시: 데이터베이스에 연결된 간단한 엔드포인트 추가
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username', '')
    
    if not username:
        logging.error('username_required222')
        logging.info('username_required222')
        
        return jsonify({'status': 'username_required'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'status': 'user_created'}), 201



@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.json
    room_id = data['room_id']
    word_list = data['word_list']
    game_manager.create_game(room_id, word_list)
    return jsonify({'status': 'room_created', 'room_id': room_id})

@socketio.on('join')
def on_join(data):
    room_id = data['room_id']
    player_id = data['player_id']
    join_room(room_id)
    game_manager.add_player(room_id, player_id)
    emit('player_joined', {'player_id': player_id}, room=room_id)

@socketio.on('guess')
def on_guess(data):
    room_id = data['room_id']
    player_id = data['player_id']
    guess = data['guess']
    
    if game_manager.check_word(room_id, guess):
        emit('correct_guess', {'player_id': player_id, 'word': guess}, room=room_id)
        game_manager.next_word(room_id)
    else:
        emit('wrong_guess', {'player_id': player_id, 'guess': guess}, room=room_id)
        game_manager.next_turn(room_id)
    
    next_player = game_manager.games[room_id]['players'][game_manager.games[room_id]['current_turn']]
    emit('next_turn', {'next_player': next_player}, room=room_id)

@socketio.on('disconnect')
def on_disconnect():
    # 플레이어가 게임에서 나갔을 때의 로직 추가 가능
    pass

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5555))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    socketio.run(app, host='0.0.0.0', port=5555, debug=debug)
