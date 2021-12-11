import os
import requests
import json
import jwt
import re
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
    message = Column(String, nullable=True)
    error_message = Column(String, nullable=False)
    source = Column(String(1024), nullable=False)
    client = Column(String, nullable=False)
    type = Column(String(2), nullable=False)

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

def check_message(message :str, block_words=[]) -> bool :
    regex_str = r'\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|OR|FROM|SET|UPDATE|UNION( +ALL){0,1})\b'
    regex_xss = r'''<[^\w<>]*(?:[^<>"'\s]*:)?[^\w<>]*(?:\W*s\W*c\W*r\W*i\W*p\W*t|\W*f\W*o\W*r\W*m|\W*s\W*t\W*y\W*l\W*e|\W*s\W*v\W*g|
    \W*m\W*a\W*r\W*q\W*u\W*e\W*e|(?:\W*l\W*i\W*n\W*k|\W*o\W*b\W*j\W*e\W*c\W*t|\W*e\W*m\W*b\W*e\W*d|\W*a\W*p\W*p\W*l\W*e\W*t|\W*p\W*a\W*r\W*a\W*m|
    \W*i?\W*f\W*r\W*a\W*m\W*e|\W*b\W*a\W*s\W*e|\W*b\W*o\W*d\W*y|\W*m\W*e\W*t\W*a|\W*i\W*m\W*a?\W*g\W*e?|\W*v\W*i\W*d\W*e\W*o|\W*a\W*u\W*d\W*i\W*o|
    \W*b\W*i\W*n\W*d\W*i\W*n\W*g\W*s|\W*s\W*e\W*t|\W*i\W*s\W*i\W*n\W*d\W*e\W*x|\W*a\W*n\W*i\W*m\W*a\W*t\W*e)[^>\w])|(?:<\w[\s\S]*[\s\0\/]|['"])(?:formaction|
    style|background|src|lowsrc|ping|on(?:d(?:e(?:vice(?:(?:orienta|mo)tion|proximity|found|light)|livery(?:success|error)|activate)|
    r(?:ag(?:e(?:n(?:ter|d)|xit)|(?:gestur|leav)e|start|drop|over)?|op)|i(?:s(?:c(?:hargingtimechange|onnect(?:ing|ed))|abled)|aling)|
    ata(?:setc(?:omplete|hanged)|(?:availabl|chang)e|error)|urationchange|ownloading|blclick)|Moz(?:M(?:agnifyGesture(?:Update|Start)?|
    ouse(?:PixelScroll|Hittest))|S(?:wipeGesture(?:Update|Start|End)?|crolledAreaChanged)|(?:(?:Press)?TapGestur|BeforeResiz)e|EdgeUI(?:C(?:omplet|
    ancel)|Start)ed|RotateGesture(?:Update|Start)?|A(?:udioAvailable|fterPaint))|c(?:o(?:m(?:p(?:osition(?:update|start|end)|lete)|mand(?:update)?)|
    n(?:t(?:rolselect|extmenu)|nect(?:ing|ed))|py)|a(?:(?:llschang|ch)ed|nplay(?:through)?|rdstatechange)|h(?:(?:arging(?:time)?ch)?ange|ecking)|
    (?:fstate|ell)change|u(?:echange|t)|l(?:ick|ose))|m(?:o(?:z(?:pointerlock(?:change|error)|(?:orientation|time)change|fullscreen(?:change|error)|
    network(?:down|up)load)|use(?:(?:lea|mo)ve|o(?:ver|ut)|enter|wheel|down|up)|ve(?:start|end)?)|essage|ark)|s(?:t(?:a(?:t(?:uschanged|echange)|
    lled|rt)|k(?:sessione|comma)nd|op)|e(?:ek(?:complete|ing|ed)|(?:lec(?:tstar)?)?t|n(?:ding|t))|u(?:ccess|spend|bmit)|peech(?:start|end)|ound(?:start|
    end)|croll|how)|b(?:e(?:for(?:e(?:(?:scriptexecu|activa)te|u(?:nload|pdate)|p(?:aste|rint)|c(?:opy|ut)|editfocus)|deactivate)|gin(?:Event)?)|
    oun(?:dary|ce)|l(?:ocked|ur)|roadcast|usy)|a(?:n(?:imation(?:iteration|start|end)|tennastatechange)|fter(?:(?:scriptexecu|upda)te|print)|
    udio(?:process|start|end)|d(?:apteradded|dtrack)|ctivate|lerting|bort)|DOM(?:Node(?:Inserted(?:IntoDocument)?|Removed(?:FromDocument)?)|
    (?:CharacterData|Subtree)Modified|A(?:ttrModified|ctivate)|Focus(?:Out|In)|MouseScroll)|r(?:e(?:s(?:u(?:m(?:ing|e)|lt)|ize|et)|adystatechange|
    pea(?:tEven)?t|movetrack|trieving|ceived)|ow(?:s(?:inserted|delete)|e(?:nter|xit))|atechange)|p(?:op(?:up(?:hid(?:den|ing)|show(?:ing|n))|state)|
    a(?:ge(?:hide|show)|(?:st|us)e|int)|ro(?:pertychange|gress)|lay(?:ing)?)|t(?:ouch(?:(?:lea|mo)ve|en(?:ter|d)|cancel|start)|ime(?:update|out)|
    ransitionend|ext)|u(?:s(?:erproximity|sdreceived)|p(?:gradeneeded|dateready)|n(?:derflow|load))|f(?:o(?:rm(?:change|input)|cus(?:out|in)?)|
    i(?:lterchange|nish)|ailed)|l(?:o(?:ad(?:e(?:d(?:meta)?data|nd)|start)?|secapture)|evelchange|y)|g(?:amepad(?:(?:dis)?connected|button(?:down|
    up)|axismove)|et)|e(?:n(?:d(?:Event|ed)?|abled|ter)|rror(?:update)?|mptied|xit)|i(?:cc(?:cardlockerror|infochange)|n(?:coming|valid|put))|
    o(?:(?:(?:ff|n)lin|bsolet)e|verflow(?:changed)?|pen)|SVG(?:(?:Unl|L)oad|Resize|Scroll|Abort|Error|Zoom)|h(?:e(?:adphoneschange|l[dp])|ashchange|
    olding)|v(?:o(?:lum|ic)e|ersion)change|w(?:a(?:it|rn)ing|heel)|key(?:press|down|up)|(?:AppComman|Loa)d|no(?:update|match)|Request|zoom))[\s\0]*='''
    sql_comment_symbol = ['--',';']
    bad_words_regex = r'\b('+ "|".join([x.lower() for x in block_words])+r')\b'
    banks_bins = ['522223','424436','521178','548673','548601','45841','415428','676371','477964','419152','525477','443888','446958',
    '427229','46223','527883','447520','548999','526483','523526','484157','511738','404757','469395','532315','544067','434914','525477',
    '405992','525744','554373','465203','416792','465204','548265','533736','540616','520905','440503','554761','485078','513691','427683','63900',
    '67758','427901','5469','427644','427601','427901','427631','531687','516331','521324','445435','518901']
    regex_dict = {
        "СНИЛС": r"\d{3}-\d{3}-\d{3} \d{2}" , 
        "Номер банковской карты": r"""(?<!\d)\d{16}(?!\d)|(?<!\d[ _-])(?<!\d)\d{4}(?:[_ -]\d{4}){3}(?![_ -]?\d)""" ,
        "Серия номер паспорта РФ": r"\d{4}\s\d{6}",
        "Адрес электронной почты": r"[a-zA-Z1-9\-\._]+@[a-z1-9]+(.[a-z1-9]+){1,}",
        "ФИО": r"([А-ЯЁ][а-яё]+[\-\s]?){3,}",
        "Телефон": r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}",
    }

    try:
        if (re.findall(regex_str,message.upper())):
            if sql_comment_symbol[0] in message or sql_comment_symbol[1] in message:
                return False, 'SI', "SQLi is detected. Message aborted"
        elif (re.findall(regex_xss,message)):
            return False, 'X', "JS code detected, maybe XSS here"
        elif (len(block_words) and re.findall(bad_words_regex,message.lower())):
            return False, 'BW', "block words detected. Message aborted"
        for key,value in regex_dict.items():
            if re.findall(value,message):
                if key == "Номер банковской карты":
                    for x in banks_bins:
                        if x in message.strip():
                            return False, "FL", f"Detected possible transfer of personal data: {key} \nPossible BIN detected"
                return False, "FL", f"Detected possible transfer of personal data: {key}"
        return True, 'OK', 'OK'
    except Exception as e:
        return False, 'U', str(e)

def validate_str_fields(data):
    valid, error_type, message = True, 'OK', 'OK'
    if isinstance(data, list):
        for v in data:
            valid, error_type, message = validate_str_fields(v)
            if not valid:
                return valid, error_type, message
    elif isinstance(data, dict):
        for v in data.values():
            valid, error_type, message = validate_str_fields(v)
            if not valid:
                return valid, error_type, message
    elif isinstance(data, str):
        return check_message(data)
    
    return valid, error_type, message

def validate_message(data, method):
    schemas = WebSocketSchema.query.filter_by(method=method)
    
    validated = False
    error_messages = []
    error_messages = [f'Method {method} not allowed']
    error_type = 'BM'
    for schema in schemas:
        error_messages = []
        try:
            validate(data, json.loads(schema.schema))
            validated = True
            break
        except BaseException as e:
            error_messages.append(str(e))
            error_type = 'IF'
            continue
    if validated:
        validated, error_type, message = validate_str_fields(data)
        error_messages.append(message)
    
    return validated, error_messages, error_type

def process_message(data, method, source, client, dttm):
    is_valid, error_messages, error_type = validate_message(data, method)

    if not is_valid:
        Violation.add(
            Violation(
                dttm=dttm, 
                error_message="\n".join(error_messages), 
                message=json.dumps(data, ensure_ascii=False),
                type=error_type,
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
        'method': method,
    }
    if callback:
        requests.post(callback.callback_url, json=data, headers=json.loads(callback.headers))


def check_origin(origin, source, client, dttm):
    allowed = bool(WebSocketAllowedOrigin.query.filter_by(name=origin).first())

    if not allowed:
        Violation.add(
            Violation(
                dttm=dttm, 
                error_message=f"Not allowed origin {origin}", 
                type='BO',
                source=source, 
                client=str(client),
                dttm_added=func.now(),
                dttm_modified=func.now(),
            )
        )
    return allowed

@socketio.on('connect')
def connect():
    addr = request.headers.get('http-x-forwarded-for', '').split(',')[0] if request.headers.get('http-x-forwarded-for') else request.remote_addr
    if not check_origin(request.origin, addr, request.args.get('token'), datetime.now()):
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
    addr = request.headers.get('http-x-forwarded-for', '').split(',')[0] if request.headers.get('http-x-forwarded-for') else request.remote_addr
    if not process_message(message.get('payload'), message.get('method'), addr, client_data, datetime.now()):
        # do some info staff
        print('bad message', message)
        disconnect()
        raise ConnectionRefusedError('Bad message')
    print('message ok')
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
