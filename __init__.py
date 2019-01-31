from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    url_for,
    flash
    )
from flask import session as login_session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Store, Product

import random
import string
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read()
    )['web']['client_id']
APPLICATION_NAME = "Store Product Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///products.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def required(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return required


@app.route('/stores/json')
def restaurant_json():
    stores = session.query(Store).all()
    return jsonify(stores=[r.serialize for r in stores])


@app.route('/store/<string:store_name>/products/json')
def products_json(store_name):
    store = session.query(Store).filter_by(name=store_name).one()
    products = session.query(Product).filter_by(store_id=store.id).all()
    return jsonify(products=[r.serialize for r in products])


@app.route('/store/<string:store_name>/product/<string:product_name>/json/')
def product_item_Json(store_name, product_name):
    store = session.query(Store).filter_by(name=store_name).one()
    products = session.query(Product).filter_by(
        store_id=store.id,
        productName=product_name
        ).one()
    return jsonify(products=[products.serialize])


# Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template(
        'login.html',
        STATE=state,
        userLogin=login_session.get('username')
        )


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
            json.dumps('Failed to upgrade the authorization code.'),
            401
            )
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
            json.dumps("Token's user ID doesn't match given user ID."),
            401
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."),
            401
            )
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

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
    output += ''' " style = "width: 300px;
                    height: 300px;
                    border-radius: 150px;
                    -webkit-border-radius: 150px;
                    -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'),
            401
            )
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    s = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % s
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected.'),
            200
            )
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        error = 'Failed to revoke token for given user.'
        response = make_response(
            json.dumps(error),
            400
            )
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/users')
@login_required
def user():
    '''show all users'''
    users = session.query(User).all()
    return render_template(
        'users.html',
        users=users,
        userLogin=login_session.get('username')
        )


@app.route('/')
@app.route('/stores')
def store():
    '''show all stores'''
    stores = session.query(Store).all()
    return render_template(
        'stores.html',
        stores=stores,
        userLogin=login_session.get('username')
        )


@app.route('/store/new', methods=['GET', 'POST'])
@login_required
def new_store():
    '''create new store'''
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        picture = request.form.get('picture')
        user_id = login_session['user_id']
        # to check if store exist
        store1 = session.query(Store).filter_by(name=name).all()
        if not store1:
            store = Store(
                name=name, description=description,
                address=address, picture=picture,
                user_id=user_id
                )
            session.add(store)
            session.commit()
            flash('new store is created')
            return redirect(url_for('store'))
        flash('this store is already exist')
        return redirect(url_for('store'))
    return render_template(
        'new_store.html',
        userLogin=login_session.get('username')
        )


@app.route('/store/<string:store_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_store(store_name):
    '''edit exist store'''
    store = session.query(Store).filter_by(name=store_name).one()
    if store.user.name != login_session['username']:
        return "you dont have permission to do this"
    if request.method == 'POST':
        store.name = request.form.get('name')
        store.description = request.form.get('description')
        store.address = request.form.get('address')
        store.picture = request.form.get('picture')
        session.add(store)
        session.commit()
        flash('edit store is done successfully')
        return redirect(url_for('store'))
    return render_template(
        'edit_store.html',
        store=store,
        userLogin=login_session.get('username')
        )


@app.route('/store/<string:store_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_store(store_name):
    '''delete exist store'''
    store = session.query(Store).filter_by(name=store_name).one()
    if store.user.name != login_session['username']:
        return "you dont have permission to do this"
    if request.method == 'POST':
        session.delete(store)
        session.commit()
        flash('delete store is done successfully')
        return redirect(url_for('store'))
    return render_template(
        'delete_store.html',
        store_name=store_name,
        userLogin=login_session.get('username')
        )


@app.route('/store/<string:store_name>/products')
def product(store_name):
    '''show all products of specific store'''
    store = session.query(Store).filter_by(name=store_name).one()
    products = session.query(Product).filter_by(store_id=store.id).all()
    return render_template(
        'products.html',
        products=products,
        store_name=store_name,
        userLogin=login_session.get('username')
        )


@app.route('/store/<string:store_name>/product/new', methods=['GET', 'POST'])
@login_required
def new_product(store_name):
    '''create new product to specific store'''
    store = session.query(Store).filter_by(name=store_name).one()
    if request.method == 'POST':
        productName = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        type_of = request.form.get('type_of')
        picture = request.form.get('picture')
        user_id = login_session['user_id']
        # to check id product is already exist
        product1 = session.query(Product).filter_by(
            store_id=store.id,
            productName=productName
            ).all()
        if not product1:
            product = Product(
                productName=productName,
                description=description,
                price=price,
                type_of=type_of,
                picture=picture,
                user_id=user_id,
                store_id=store.id
                )
            session.add(product)
            session.commit()
            flash('new product is created')
            return redirect(url_for('product', store_name=store_name))
        else:
            flash('this product is already exist')
            return redirect(url_for('product', store_name=store_name))
    return render_template(
        'new_product.html',
        store_name=store_name,
        userLogin=login_session.get('username')
        )


@app.route(
    '/store/<string:store_name>/<string:product_name>/edit',
    methods=['GET', 'POST']
    )
@login_required
def edit_product(store_name, product_name):
    '''edit exist product on specific store'''
    store = session.query(Store).filter_by(name=store_name).one()
    product = session.query(Product).filter_by(
        store_id=store.id,
        productName=product_name
        ).one()
    if product.user.name != login_session['username']:
        return "you dont have permission to do this"
    if request.method == 'POST':
        product.productName = request.form.get('name')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        product.type_of = request.form.get('type_of')
        product.picture = request.form.get('picture')
        product.user_id = login_session['user_id']
        product.store_id = store.id
        session.add(product)
        session.commit()
        flash('edit product is done successfully')
        return redirect(url_for('product', store_name=store_name))
    return render_template(
        'edit_product.html',
        store_name=store_name,
        product=product,
        userLogin=login_session.get('username')
        )


@app.route(
    '/store/<string:store_name>/<string:product_name>/delete',
    methods=['POST', 'GET']
    )
@login_required
def delete_product(store_name, product_name):
    '''edit exist product on specific store'''
    store = session.query(Store).filter_by(name=store_name).one()
    product = session.query(Product).filter_by(
        store_id=store.id,
        productName=product_name
        ).one()
    if product.user.name != login_session['username']:
        return "you dont have permission to do this"
    if request.method == 'POST':
        session.delete(product)
        session.commit()
        flash('delete product is done successfully')
        return redirect(url_for('product', store_name=store_name))
    return render_template(
        'delete_product.html',
        store_name=store_name,
        product_name=product_name,
        userLogin=login_session.get('username')
        )


# helper function
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
        )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# run server
if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='127.0.0.1', port=8000)
