from flask import Flask
from main_handlers.catalog import catalog_page
from login_handlers.oauth_login import oauth_page
from menu import menu_page

app = Flask(__name__)
app.register_blueprint(catalog_page)
app.register_blueprint(oauth_page)
app.register_blueprint(menu_page)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)