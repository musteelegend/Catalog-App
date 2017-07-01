from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, Blueprint
from flask_login import login_user , logout_user
app = Flask(__name__)

from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


from login_handlers.oauth_login import showLogin, gconnect, fbconnect

oauth_logout_page = Blueprint('oauth_logout_page', __name__,
                        template_folder='templates')

@oauth_logout_page.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@oauth_logout_page.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@oauth_logout_page.route('/logout')
def logout():
    logout_user()


# Disconnect based on provider
@oauth_logout_page.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['picture']
            del login_session['user_id']
            #del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['picture']
            del login_session['user_id']
        if login_session['provider'] == 'inHouse':
            logout()
        del login_session['username']
        del login_session['email']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('catalog_page.showCatalogs'))
    else:
        flash("You were not logged in")
        return redirect(url_for('catalog_page.showCatalogs'))
