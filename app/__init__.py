from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask import request
from flask_babel import lazy_gettext as _l

app = Flask (__name__) # __name__ это имя текщего файла (__init.py__ ?) от этого пути Фласк будет отталкиватся и находить другие файлы (шалоны цсс и тд)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
bootstrap = Bootstrap(app)
login.login_view = 'login'
moment = Moment(app)
babel = Babel(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
    

@babel.localeselector
def get_locale():
    #return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'es'

from app import routes, models, errors


# Один из аспектов, который может показаться запутанным вначале, состоит в том, что существуют два объекта с именем app.
# Пакет приложения определяется каталогом приложения и сценарием __init__.py и указан в инструкции routes импорта приложения. 
# Переменная app определяется как экземпляр класса Flask в сценарии __init__.py, что делает его частью пакета приложения.


# Другая особенность заключается в том, что модуль routes импортируется внизу, а не наверху скрипта, как это всегда делается. 
# Нижний импорт является обходным путем для циклического импорта, что является общей проблемой при использовании приложений Flask. 
# Вы увидите, что модуль routes должен импортировать переменную приложения, определенную в этом скрипте, поэтому, поместив один из 
# взаимных импортов внизу, вы избежите ошибки, которая возникает из взаимных ссылок между этими двумя файлами.