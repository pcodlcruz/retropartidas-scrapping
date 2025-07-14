import os

def get_session_cookie():
    return os.getenv('RETROPARTIDAS_SESSION_COOKIE')

def get_url_paths():
    return os.getenv('RETROPARTIDAS_URL_PATHS').split(',')

def get_base_url():
    return 'https://retropartidas.inforpsico.com/'


