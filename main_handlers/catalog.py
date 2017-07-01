from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint
app = Flask(__name__)

from flask import session as login_session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, MenuItem, OauthUser
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



catalog_page = Blueprint('catalog_page', __name__,
                        template_folder='templates')

@catalog_page.route('/')
@catalog_page.route('/catalog/')
def showCatalogs():
  catalogs = session.query(Catalog).order_by(asc(Catalog.name))
  latestItems = session.query(MenuItem).order_by(desc(MenuItem.created_date)).limit(8)
  if 'username' not in login_session:
      return render_template('publiccatalogs.html', catalogs=catalogs, latestItems=latestItems)
  else:
      return render_template('catalogs.html', catalogs = catalogs, latestItems=latestItems)


#Create a new catalog
@catalog_page.route('/catalog/new/', methods=['GET','POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(name = request.form['name'], user_id=login_session['user_id'])
        session.add(newCatalog)
        flash('New Catalog %s Successfully Created' % newCatalog.name)
        session.commit()
        return redirect(url_for('catalog_page.showCatalogs'))
    else:
        return render_template('newcatalog.html')

#Edit a catalog
@catalog_page.route('/catalog/<int:catalog_id>/edit/', methods = ['GET', 'POST'])
def editCatalog(catalog_id):
    editedCatalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCatalog.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this catalog. Please create your own catalog in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        editedCatalog.name = request.form['name']
        session.add(editedCatalog)
        session.commit()
        flash('Catalog Successfully Edited %s' % editedCatalog.name)
        return redirect(url_for('menu_page.showMenu', catalog_id=catalog_id))
    else:
        return render_template('editcatalog.html', catalog = editedCatalog)


#Delete a catalog
@catalog_page.route('/catalog/<int:catalog_id>/delete/', methods = ['GET','POST'])
def deleteCatalog(catalog_id):
    catalogToDelete = session.query(Catalog).filter_by(id = catalog_id).one()
    # menuItemsToDelete = session.query(MenuItem).filter_by(catalog_id=catalog_id).all()
    if 'username' not in login_session:
        return redirect('/login')
    if catalogToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this catalog. Please create your own catalog in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
      session.delete(catalogToDelete)
      # for i in menuItemsToDelete:
      #     session.delete(i)
      flash('%s Successfully Deleted' % catalogToDelete.name)
      session.commit()
      return redirect(url_for('catalog_page.showCatalogs'))
    else:
      return render_template('deleteCatalog.html', catalog=catalogToDelete)
