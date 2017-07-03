from flask import Flask
from main_handlers.catalog import catalog_page
from login_handlers.oauth_login import oauth_login_page
from logout_handlers.oauth_logout import oauth_logout_page
from database.database_setup import Base, User
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from main_handlers.menu import menu_page
from REST_handlers.catalogs_menuitem_JSON import json_page
from flask_login import LoginManager

engine = create_engine('sqlite:///catalogmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))

app.register_blueprint(catalog_page)
app.register_blueprint(oauth_login_page)
app.register_blueprint(menu_page)
app.register_blueprint(oauth_logout_page)
app.register_blueprint(json_page)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
