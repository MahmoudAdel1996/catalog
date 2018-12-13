from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Store, Product

engine = create_engine('sqlite:///products.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy users
users = [
    {
        'name': "Robo Barista",
        'email': "tinnyTim@udacity.com",
        'picture': 'https://goo.gl/i8MA1u'
    },
    {
        'name': "bill gates",
        'email': "billGates@udacity.com",
        'picture': 'https://goo.gl/EY7Fz1'
    },
    {
        'name': "james gosling",
        'email': "jamesGosling@udacity.com",
        'picture': 'https://goo.gl/jDPFfw'
    },
    {
        'name': "Mark Zuckerberg",
        'email': "MarkZuckerberg@udacity.com",
        'picture': 'https://goo.gl/UE8qiB'
    }
]

for user in users:
    create_users = User(
        name=user['name'],
        email=user['email'],
        picture=user['picture']
        )
    session.add(create_users)
    session.commit()


stors = [
    {
        'name': 'Carfoure',
        'description': 'Hyper Market',
        'address': 'Egypt',
        'picture': 'https://goo.gl/YbSSxf',
        'user_id': 1
    },
    {
        'name': 'Fathla',
        'description': 'Hyper Market',
        'address': 'Egypt',
        'picture': 'https://goo.gl/Axf43z',
        'user_id': 2
    },
    {
        'name': 'Amazon',
        'description': 'Hyper Market',
        'address': 'America',
        'picture': 'https://goo.gl/859mnc',
        'user_id': 3
    },
    {
        'name': 'Souq',
        'description': 'Hyper Market',
        'address': 'America',
        'picture': 'https://goo.gl/9DWxsY',
        'user_id': 4
    },
    {
        'name': 'Microsoft',
        'description': 'electronic',
        'address': 'America',
        'picture': 'https://goo.gl/nzPwEx',
        'user_id': 2
    },
]

for store in stors:
    create_store = Store(
        name=store['name'],
        description=store['description'],
        address=store['address'],
        picture=store['picture'],
        user_id=store['user_id']
        )
    session.add(create_store)
    session.commit()

products = [
    {
        'name': 'Tomato',
        'description': 'Organic Greenhouse Red On-The-Vine Tomatoes',
        'price': '2',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/qgCvYx',
        'user_id': 1,
        'store_id': 1
    },
    {
        'name': 'Onion',
        'description': 'Onions can boost up the taste and flavors of dishes',
        'price': '5',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/Zqahbr',
        'user_id': 2,
        'store_id': 1
    },
    {
        'name': 'Potato',
        'description': 'Fresh food',
        'price': '4',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/6Hr23y',
        'user_id': 3,
        'store_id': 1
    },
    {
        'name': 'Tomato',
        'description': 'Organic Greenhouse Red On-The-Vine Tomatoes',
        'price': '2',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/qgCvYx',
        'user_id': 1,
        'store_id': 2
    },
    {
        'name': 'Onion',
        'description': 'Onions can boost up the taste and flavors of dishes',
        'price': '5',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/Zqahbr',
        'user_id': 2,
        'store_id': 3
    },
    {
        'name': 'Potato',
        'description': 'Fresh food',
        'price': '4',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/6Hr23y',
        'user_id': 3,
        'store_id': 4
    },
    {
        'name': 'Tomato',
        'description': 'Organic Greenhouse Red On-The-Vine Tomatoes',
        'price': '2',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/qgCvYx',
        'user_id': 1,
        'store_id': 5
    },
    {
        'name': 'Onion',
        'description': 'Onions can boost up the taste and flavors of dishes',
        'price': '5',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/Zqahbr',
        'user_id': 2,
        'store_id': 4
    },
    {
        'name': 'Potato',
        'description': 'Fresh food',
        'price': '4',
        'type_of': 'Organic',
        'picture': 'https://goo.gl/6Hr23y',
        'user_id': 3,
        'store_id': 2
    },
]

for product in products:
    create_product = Product(
        productName=product['name'],
        description=product['description'],
        price=product['price'],
        type_of=product['type_of'],
        picture=product['picture'],
        user_id=product['user_id'],
        store_id=product['store_id']
        )
    session.add(create_product)
    session.commit()

session.close()
print("added data items!")
