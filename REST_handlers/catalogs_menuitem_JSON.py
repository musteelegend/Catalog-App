from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, MenuItem, OauthUser
from login_handlers.oauth_login import showLogin, fbconnect, gconnect
# IMPORTS FOR THIS STEP
import json
from flask import make_response
import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for,
flash, Blueprint


engine = create_engine('sqlite:///catalogmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

json_page = Blueprint('json_page', __name__, template_folder='templates')


# JSON APIs to view catalog Information
@json_page.route('/catalog/<int:catalog_id>/menu/JSON')
def catalogMenuJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(MenuItem).filter_by(catalog_id=catalog_id).all()
    return jsonify(catalog=catalog.serialize,
                   MenuItems=[i.serialize for i in items])


@json_page.route('/catalog/<int:catalog_id>/menu/<string:item_title>/JSON')
def menuItemJSON(catalog_id, item_title):
    Menu_Item = session.query(MenuItem).filter_by(title=item_title).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@json_page.route('/catalog/JSON')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])
