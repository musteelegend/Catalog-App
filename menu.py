from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint
app = Flask(__name__)

from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, MenuItem, User
from login_handlers.oauth_login import showLogin, fbconnect, gconnect


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
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', items=items, catalog=catalog, catalogs=catalogs, creator=creator)
    else:
        return render_template('menu.html', items = items, catalog = catalog, catalogs=catalogs, creator=creator)



#Create a new menu item
@menu_page.route('/catalog/menu/new/',methods=['GET','POST'])
def newMenuItem():
  if 'username' not in login_session:
      return redirect('/login')
  # catalogs = session.query(Catalog).order_by(asc(Catalog.name))
  # if login_session['user_id'] != catalog.user_id:
      # return "<script>function myFunction() {alert('You are not authorized to add menu items to this catalog. Please create your own catalog in order to add items.');}</script><body onload='myFunction()''>"
  catalogs = request.args.get('catalogs')
  if request.method == 'POST':
      newItem = MenuItem(title = request.form['title'], description = request.form['description'], catalog_id = catalog_id, user_id=login_session['user_id'])
      session.add(newItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('menu_page.showMenu'))
  else:
      return render_template('newmenu.html')


#Edit a menu item
@menu_page.route('/catalog/<int:catalog_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(catalog_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this catalog. Please create your own catalog in order to edit items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('menu_page.showMenu', catalog_id = catalog_id))
    else:
        return render_template('editmenuitem.html', catalog_id = catalog_id, menu_id = menu_id, item = editedItem)


#Delete a menu item
@menu_page.route('/catalog/<int:catalog_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(catalog_id,menu_id):
    if 'username' not in login_session:
       return redirect('/login')
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this catalog. Please create your own catalog in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', catalog_id=catalog_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)