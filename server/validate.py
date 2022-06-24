import re, datetime

def password_check(password):
    error_message_list = []
    if len(password) < 10:
        error_message_list.append('10 characters length or more')
    if re.search(r"\d", password) is None:
        error_message_list.append('1 numeral or more')
    if re.search(r"[A-Z]", password) is None:
        error_message_list.append('1 uppercase letter or more')
    if re.search(r"[a-z]", password) is None:
        error_message_list.append('1 lowercase letter or more')
    if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
        error_message_list.append('1 symbol or more')

    return {
        'password_ok' : len(error_message_list) == 0,
        'msg': ', '.join(str(x) for x in error_message_list) 
    }

def date_check(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d').date()
    except:
        return None

LoginSchema = {
    'type': 'object',
    'properties': {
        'username': { 'type': 'string' },
        'password': { 'type': 'string' }
    },
    'required': ['username', 'password']
}

RegisterSchema = {
    'type': 'object',
    'properties': {
        'name':     { 'type': 'string' },
        'username': { 'type': 'string' },
        'password': { 'type': 'string' }
    },
    'required': ['name', 'username', 'password']
}

PasswordChangeSchema = {
    'type': 'object',
    'properties': {
        'password': { 'type': 'string' }
    },
    'required': ['password']
}

CleanerSchema = {
    'type': 'object',
    'properties': {
        'badge': { 'type': 'string' },
        'name':  { 'type': 'string' }
    },
    'required': ['badge', 'name']
}

BookingSchema = {
    'type': 'object',
    'properties': {
        'cleaner_id': { 'type': 'number' },
        'date':       { 'type': 'string' }
    },
    'required': ['cleaner_id', 'date']
}
