import os
import requests
import json
import jwt
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO, ConnectionRefusedError, disconnect
from flask_sqlalchemy import SQLAlchemy
from jsonschema import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qLLh_9qTRQqCYzydSKWmmA'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.root_path, 'db', 'db.sqlite3')
JWT_SECRET = os.environ.get('JWT_SECRET', 'secret!')
SERVER_TOKEN = os.environ.get('SERVER_TOKEN', 'secret_server_token!')
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)
db = SQLAlchemy(app)


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return e

class Base(db.Model):
    __abstract__ = True

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @staticmethod
    def get(self, id):
        return self.query.filter_by(id=id).first()

    @staticmethod
    def remove_session():
        db.session.close()

    @staticmethod
    def add(model):
        db.session.add(model)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self):
        self.query.filter_by(id=self.id).delete()
        return session_commit()


class WebSocketSchema(Base):
    __tablename__ = 'websocket_websocketschema'

    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)
    code = Column(String(512), nullable=True)
    dttm_added = Column(DateTime)
    dttm_modified = Column(DateTime)
    schema = Column(String, nullable=False)
    method = Column(String(1024), nullable=False)

class Violation(Base):
    __tablename__ = 'websocket_websocketviolation'

    id = Column(Integer, primary_key=True)
    dttm = Column(DateTime, nullable=False)
    dttm_added = Column(DateTime, server_default=func.now())
    dttm_modified = Column(DateTime, onupdate=func.now())
    message = Column(String, nullable=False)
    source = Column(String(1024), nullable=False)
    client = Column(String, nullable=False)

class WebSocketCallback(Base):
    __tablename__ = 'websocket_websocketcallback'

    id = Column(Integer, primary_key=True)
    method = Column(String(512), nullable=False)
    callback_url = Column(String(1024), nullable=False)
    headers = Column(String, nullable=True)

class WebSocketAllowedOrigin(Base):
    __tablename__ = 'websocket_websocketallowedorigin'

    id = Column(Integer, primary_key=True)
    name = Column(String(1024), nullable=False)

class BaseAuth:
    def __init__(self, token):
        self.token = token
    
    def authenticate(self):
        raise NotImplementedError()

class JWTAuth(BaseAuth):
    def authenticate(self):
        authenticated = False
        client_data = {}
        try:
            client_data = jwt.decode(self.token, JWT_SECRET, algorithms=["HS256"])
            authenticated = True
        except:
            pass
        return authenticated, client_data

class ServerTokenAuth(BaseAuth):
    def authenticate(self):
        return self.token == SERVER_TOKEN

def validate_message(data, method):
    schemas = WebSocketSchema.query.filter_by(method=method)
    
    validated = False
    error_messages = []
    error_messages = [f'Method {method} not allowed']
    for schema in schemas:
        error_messages = []
        try:
            validate(data, json.loads(schema.schema))
            validated = True
            break
        except BaseException as e:
            error_messages.append(str(e))
            continue
    
    return validated, error_messages

def process_message(data, method, source, client, dttm):
    is_valid, error_messages = validate_message(data, method)

    if not is_valid:
        Violation.add(
            Violation(
                dttm=dttm, 
                message="\n".join(error_messages), 
                source=source, 
                client=str(client),
                dttm_added=func.now(),
                dttm_modified=func.now(),
            )
        )
        return False
    return True

def send_message(data, method, client):
    callback = WebSocketCallback.query.filter_by(method=method).first()
    data = {
        'client': client,
        'payload': data,
    }
    if callback:
        requests.post(callback.callback_url, json=data, headers=json.loads(callback.headers))


def check_origin(origin, source, client, dttm):
    allowed = bool(WebSocketAllowedOrigin.query.filter_by(name=origin).first())

    if not allowed:
        Violation.add(
            Violation(
                dttm=dttm, 
                message=f"Not allowed origin {origin}", 
                source=source, 
                client=str(client),
                dttm_added=func.now(),
                dttm_modified=func.now(),
            )
        )
    return allowed

@socketio.on('connect')
def connect():
    if not check_origin(request.origin, request.remote_addr, request.args.get('token'), datetime.now()):
        disconnect()
        raise ConnectionRefusedError('Bad origin')
    authenticated, _ = JWTAuth(request.args.get('token', '')).authenticate()
    if not authenticated:
        disconnect()
        raise ConnectionRefusedError('Unathorized')

@socketio.on('message')
def handle_message(message):
    authenticated, client_data = JWTAuth(request.args.get('token', '')).authenticate()
    if not authenticated:
        disconnect()
        raise ConnectionRefusedError('Unathorized')
    if not process_message(message.get('payload'), message.get('method'), request.remote_addr, client_data, datetime.now()):
        # do some info staff
        disconnect()
        raise ConnectionRefusedError('Bad message')
    send_message(message.get('payload'), message.get('method'), client_data)

@app.route('/api', methods=['post'])
def websocket_api():
    data = request.json
    if not ServerTokenAuth(data.get('token')).authenticate():
        return jsonify(error='Unauthorized!'), 400
    # Do some send staff with json from server
    socketio.emit(data.get('method'), data.get('payload'))

    return jsonify(data)

if __name__ == '__main__':
    socketio.run(app)
