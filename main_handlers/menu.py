from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint
app = Flask(__name__)

from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, MenuItem, OauthUser
from login_handlers.oauth_login import showLogin, fbconnect, gconnect, getUserInfo


# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

engine = create_engine('sqlite:///catalogmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



menu_page = Blueprint('menu_page', __name__,
                        template_folder='templates')



#Show a catalog menu
@menu_page.route('/catalog/<int:catalog_id>/')
@menu_page.route('/catalog/<int:catalog_id>/menu/')
def showMenu(catalog_id):
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    creator = getUserInfo(catalog.user_id)
    items = session.query(MenuItem).filter_by(catalog_id = catalog_id).all()
    count = session.query(MenuItem).filter_by(catalog_id = catalog_id).count()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', count=count, items=items, catalog=catalog, catalogs=catalogs, creator=creator)
    else:
        return render_template('menu.html', count=count, items=items, catalog=catalog, catalogs=catalogs, creator=creator)


#Show a catalog menu item
@menu_page.route('/catalog/<int:catalog_id>/<string:item_title>/')
@menu_page.route('/catalog/<int:catalog_id>/menu/<string:item_title>/')
def showMenuItem(catalog_id, item_title):
    # catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    creator = getUserInfo(catalog.user_id)
    item = session.query(MenuItem).filter_by(title = item_title).one()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenuitem.html', item=item, catalog=catalog, creator=creator)
    else:
        return render_template('menuitem.html', item=item, catalog = catalog, creator=creator)


#Create a new menu item
@menu_page.route('/catalog/menu/new/',methods=['GET','POST'])
def newMenuItem():
    if 'username' not in login_session:
        return redirect('/login')
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    # if login_session['user_id']:
    #     return "<script>function myFunction() {alert('You are not authorized to add menu items to this catalog. Please create your own catalog in order to add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        catalog_id = request.form.get('catalog_id')
        newItem = MenuItem(title = request.form['title'], description = request.form['description'], catalog_id = request.form['catalog_id'], user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.title))
        return redirect(url_for('menu_page.showMenu', catalog_id=catalog_id))
    else:
        return render_template('newmenu.html', catalogs=catalogs)


#Edit a menu item
@menu_page.route('/catalog/<int:catalog_id>/menu/<string:item_title>/edit', methods=['GET','POST'])
def editMenuItem(catalog_id, item_title):
    if 'username' not in login_session:
        return redirect('/login')
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    editedItem = session.query(MenuItem).filter_by(title = item_title).one()
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this catalog. Please create your own catalog in order to edit items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['catalog_id']:
            editedItem.catalog_id = request.form['catalog_id']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('menu_page.showMenuItem', item_title=item_title, catalog_id=catalog_id))
    else:
        return render_template('editmenuitem.html', catalog = catalog, item = editedItem, catalogs=catalogs)


#Delete a menu item
@menu_page.route('/catalog/<int:catalog_id>/menu/<string:item_title>/delete', methods = ['GET','POST'])
def deleteMenuItem(catalog_id,item_title):
    if 'username' not in login_session:
       return redirect('/login')
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    itemToDelete = session.query(MenuItem).filter_by(title=item_title).one()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this catalog. Please create your own catalog in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('menu_page.showMenu', catalog_id=catalog_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete, catalog=catalog)