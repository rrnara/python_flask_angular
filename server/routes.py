# Flask modules
from flask               import request, send_from_directory, jsonify
# from flask_login         import login_user, logout_user, login_required
# from werkzeug.exceptions import HTTPException, NotFound, abort
# from jinja2              import TemplateNotFound
from flask_expects_json  import expects_json
from functools           import wraps
from datetime            import datetime, timedelta, date
import jwt

# App modules
from server              import app, bc
from server.fixIndexHTML import appPath
from server.models       import Bookings, Users, USER_ROLE, ADMIN_ROLE, Cleaners
from server.validate     import LoginSchema, PasswordChangeSchema, RegisterSchema, CleanerSchema, BookingSchema, password_check, date_check

# provide login manager with load_user callback
# @lm.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))

# Logout user
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({ 'message' : 'Missing token' }), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], ['HS256'])
            print(data)
            current_user = Users.query.filter_by(id=data['id']).first()
            if current_user is None:
                return jsonify({ 'message' : 'Invalid token' }), 401
        except:
            return jsonify({ 'message' : 'Invalid token' }), 401

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)
  
    return decorated

def addUser(request, role):
    jsonData = request.get_json()
    msg      = None
    success  = False

    username = jsonData['username']
    password = jsonData['password']
    name     = jsonData['name']

    # filter User out of database through username
    user = Users.query.filter_by(username=username).first()
    if user:
        msg = 'User already exists'
    else:
        error_list = []
        if len(name) < 8:
            error_list.append('Name needs to 6 characters')
        if len(username) < 6:
            error_list.append('Username needs to 6 characters')
        
        pwCheck = password_check(password)
        if pwCheck['password_ok'] is False:
            pwmsg = pwCheck['msg']
            error_list.append(f'Password needs {pwmsg}.')
        
        if error_list.count == 0:
            pw_hash = bc.generate_password_hash(password)
            user = Users(name, username, pw_hash, role)
            user.save()
            msg     = 'User created'
            success = True
        else:
            msg = "; ".join(str(x) for x in error_list) 

    return {
        "msg": msg,
        "success": success
    }

# Register a new user
@app.route('/api/auth/register', methods=['POST'])
@expects_json(RegisterSchema)
def register():
    return addUser(request, USER_ROLE)

# Authenticate user
@app.route('/api/auth/login', methods=['POST'])
@expects_json(LoginSchema)
def login():
    jsonData = request.get_json()
    msg      = "Wrong username or password. Please try again."
    success  = False

    # check if both http method is POST and form is valid on submit
    username = jsonData['username']
    password = jsonData['password']

    # filter User out of database through username
    user = Users.query.filter_by(username=username).first()
    if user:
        if bc.check_password_hash(user.password, password):
            msg = jwt.encode({ 'id': user.id, 'exp' : datetime.utcnow() + timedelta(minutes = 180) }, app.config['SECRET_KEY'], 'HS256')
            success = True

    return {
        "msg": msg,
        "success": success,
        "user": user.to_dict() if success else None
    }

@app.route('/api/auth/admin', methods =['POST'])
@expects_json(RegisterSchema)
@token_required
def add_admin(current_user):
    if current_user.role == ADMIN_ROLE:
        return addUser(request, ADMIN_ROLE)
    else:
        return jsonify({
            "msg": "Unauthorized",
            "success": False,
            "password_check": None
        }), 401

@app.route('/api/auth/password', methods =['POST'])
@expects_json(PasswordChangeSchema)
@token_required
def update_password(current_user):
    jsonData = request.get_json()
    msg      = None
    success  = False

    password = jsonData['password']
    pwCheck = password_check(password)
    if pwCheck['password_ok'] is False:
        pwmsg = pwCheck['msg']
        msg = f'Password needs {pwmsg}.'
    else:
        pw_hash = bc.generate_password_hash(password)
        current_user.password = pw_hash
        current_user.commit()
        msg = 'Updated'
        success = True

    return {
        "msg": msg,
        "success": success
    }

@app.route('/api/users/me', methods =['GET'])
@token_required
def get_me(current_user):
    return current_user.to_dict()

@app.route('/api/users/all', methods =['GET'])
@token_required
def get_all_users(current_user):
    if current_user.role == ADMIN_ROLE:
        role = request.args['role'] if 'role' in request.args else None
        users = Users.query.filter_by(role=role) if role else Users.query.all()
        output = []
        for user in users:
            # appending the user data json to the response list, if not current user
            if user.id != current_user.id:
                output.append(user.to_dict())
        return { 'users': output, "success": True }
    else:
        return jsonify({
            "msg": "Unauthorized",
            "success": False
        }), 401


@app.route('/api/users/cleaners', methods =['POST'])
@expects_json(CleanerSchema)
@token_required
def create_cleaner(current_user):
    if current_user.role == ADMIN_ROLE:
        jsonData = request.get_json()
        badge    = jsonData['badge']
        name     = jsonData['name']
        cleaner = Cleaners.query.filter_by(badge=badge).first()
        if cleaner:
            return {
                "msg": "Cleaner already exists",
                "success": False,
                "cleaner": None
            }
        else:
            cleaner = Cleaners(badge, name)
            cleaner.save()
            return {
                "msg": "Cleaner created",
                "success": True,
                "cleaner": cleaner.to_dict()
            }
    else:
        return jsonify({
            "msg": "Unauthorized",
            "success": False
        }), 401

@app.route('/api/users/cleaners', methods =['GET'])
@token_required
def get_available_cleaners(current_user):
    cleaners = None
    if current_user.role == ADMIN_ROLE:
        cleaners = Cleaners.query.all()
    else:
        date_available = request.args['date']
        py_date    = date_check(date_available)
        if py_date is None or py_date < date.today():
            return {
                "msg": "Invalid Date Format, should be yyyy-mm-dd" if py_date is None else "Date should be in future",
                "success": False,
                "cleaners": None
            }
        existing = Bookings.query.with_entities(Bookings.cleaner_id).distinct().filter_by(date_booked=date_available)
        cleaners = Cleaners.query.filter(Cleaners.id.not_in(existing))
    output = []
    for cleaner in cleaners:
        output.append(cleaner.to_dict())
    return { 'cleaners': output, "success": True }

@app.route('/api/users/bookings', methods =['POST'])
@expects_json(BookingSchema)
@token_required
def create_booking(current_user):
    if current_user.role == ADMIN_ROLE:
        return jsonify({
            "msg": "Booking is for users",
            "success": False
        }), 409
    else:
        jsonData     = request.get_json()
        cleaner_id   = jsonData['cleaner_id']
        date_to_book = jsonData['date']
        py_date      = date_check(date_to_book)
        if py_date is None or py_date < date.today():
            return {
                "msg": "Invalid Date Format, should be yyyy-mm-dd" if py_date is None else "Date should be in future",
                "success": False,
                "booking": None
            }
        booking = Bookings.query.filter_by(date_booked=date_to_book, cleaner_id=cleaner_id).first()
        if booking:
            return {
                "msg": "Booking already exists",
                "success": False,
                "booking": None
            }
        else:
            cleaner = Cleaners.query.get(cleaner_id)
            if cleaner:
                booking = Bookings(current_user, py_date, cleaner)
                booking.save()
                return {
                    "msg": "Booking created",
                    "success": True,
                    "booking": booking.to_dict(False)
                }
            else:
                return {
                    "msg": "Cleaner not found",
                    "success": False,
                    "booking": None
                }

@app.route('/api/users/bookings', methods =['GET'])
@token_required
def get_bookings(current_user):
    bookings = []
    isAdmin = current_user.role == ADMIN_ROLE
    if isAdmin:
        date_booked = request.args['date']
        if date_check(date_booked) is None:
            return {
                "msg": "Invalid Date Format, should be yyyy-mm-dd",
                "success": False,
                "bookings": None
            }
        bookings = Bookings.query.filter_by(date_booked=date_booked)
    else:
        bookings = Bookings.query.filter_by(user_id=current_user.id).filter(Bookings.date_booked>=date.today())
    output = []
    for booking in bookings:
        output.append(booking.to_dict(isAdmin))
    return { 'bookings': output, "success": True }

# App main route + generic routing
@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def index(path):
    if path.startswith('api'):
        return jsonify({ 'path' : path }), 404
    if request.args:
        key = list(request.args)[0]
        return send_from_directory(f"{appPath}/app/dist/app", key)
    else:
        return send_from_directory(f"{appPath}/app/dist/app", "index.html")
