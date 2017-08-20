#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask import session as login_session
import random, string, requests

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User
import os

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


engine = create_engine('sqlite:///productlistwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# see if user exists. if does not, create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# API endpoint (GET request) view Category info
@app.route('/categorys/<int:category_id>/product/json')
def categoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Product).filter_by(category_id = category_id).all()
    return jsonify(Product = [i.serialize for i in items])

# JSON ENDPOINT HERE
@app.route('/categorys/<int:category_id>/product/<int:product_id>/json')
def productListJSON(category_id, _id):
    Product = session.query(Product).filter_by(id = product_id).one()
    return jsonify(Product = Product.serialize)


@app.route('/test')
def DefaultCategoryList():
    category = session.query(Category).first()
    items = session.query(Product).filter_by(category_id = category.id)
    output = ''
    for i in items:
        # output += str(category.id)
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output


# @app.route('/catalog/json')
#     return

# @app.route('/category/<int:category_id>/')
# def categoryproduct_test(category_id):
#     category = session.query(category).filter_by(id = category_id).one()
#     items = session.query(Product).filter_by(category_id = category.id)
#     output = ''
#     for item in items:
#         output += item.name
#         output += '</br>'
#         output += item.price
#         output += '</br>'
#         output += item.description
#         output += '</br>'
#         output += '</br>'
#     return output

@app.route('/catalog/<int:category_id>/')
def categoryProduct(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Product).filter_by(category_id = category.id)
    return render_template('category.html', category = category, items = items) ## menu.html

# show all categorys
@app.route('/')
@app.route('/catalog')
def showCategorys():
    #category = session.query(Category).filter_by(id = category_id).one()
    categorys = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publicCategories.html', categorys = categorys)
    else:
        return render_template('Categories.html', categorys = categorys)


# Create a new category
@app.route('/category/new')
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcategory = category(name = request.form['name'])
        session.add(category)
        flash('New Category Successfully Created')
        session.commit()
        return redirect(url_for('showCategory.html'))
    else:
        return render_template('newCategory.html')


# # Edit a category
# @app.route('/<int:category_id>/edit')
# def editCategory(category_id):
# 	# return "This page will be for editing category %s " % category_id
#     return render_template('editCategory.html', category_id = category_id)


# delete a category
@app.route('/<int:category_id>/delete')
@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own account in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategorys', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)
    # return "This page will be for deleting category %s" %category_id
    return render_template('deleteCategory.html', category_id = category_id)


# # show a category product
# @app.route('/<int:category_id>/product')
# @app.route('/category/<int:category_id>/product')     ## 'category<int:category_id>/product'
# def showProduct(category_id):
#     # return "This page is the product for category %s" %category_id
#     category = session.query(Category).filter_by(id=category_id).one()
#     creator = getUserInfo(category.user_id)
#     items = session.query(Product).filter_by(category_id=category_id).all()
#     if 'username' not in login_session or creator.id != login_session['user_id']:
#         return render_template('publicProduct.html', items=items, category=category, creator=creator)
#     else:
#         return render_template('product.html', items=items, category=category, creator=creator)
#     return render_template('product.html', category_id = category_id)


# @app.route('/category/category_id/product/new')
@app.route('/category/<int:category_id>/new', methods = ['GET', 'POST'])
def newProduct(category_id):
    # return "This page is for making new product item for category %s" %category_id
    if request.method == 'POST':
        newProduct = Product(name=request.form['name'], description=request.form[      #newItem
                           'description'], price=request.form['price'], 
                           course=request.form['course'], 
                           category_id=category_id)
        session.add(newProduct)                  #newItem
    	session.commit()
    	flash("New product added!")
    	return redirect(url_for('categoryProduct', category_id = category_id))
    else:
    	return render_template('newProduct.html', category_id = category_id)


@app.route('/category/<int:category_id>/product/<int:product_id>/edit/', methods = ['GET', 'POST'])
def editProduct(category_id, product_id):
    # return "This page is for editing product item %s" %product_id
    editedItem = session.query(Product).filter_by(id = product_id).one()
    if request.method == 'POST':
    	if request.form['name']:
            editedItem.name['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('categoryProduct', category_id = category_id))
    else:
        return render_template('editProduct.html', 
                                category_id = category_id, 
                                product_id = product_id, item = editedItem)

@app.route('/category/<int:category_id>/product/<int:product_id>/delete', methods = ['GET', 'POST'])
def deleteProduct(category_id, product_id):
    itemToDelete = session.query(Product).filter_by(id=product_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item % deleted") % itemToDelete
        return redirect(url_for('categoryProduct', category_id=category_id))
    else:
        return render_template('deleteConfirmation.html', item=itemToDelete)


def createUser(login_session):
    newUser = User(name=login_session['username'], 
                    email=login_session['email'], 
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port =8000)
