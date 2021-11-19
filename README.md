# Item-Catalog
by Mahmoud Adel, in fulfillment of Udacity's

## Description
This project can preview all stores on the world with address, can preview
all products that already exist in a specific store, and many features when
user is logged in then he have a permission to create, edit, delete store
and product but he can delete and edit only things he was created before,
developed by `Python Flask Framework` with persistent data storage `SQLite Database`.

## Getting Started

### Prerequisites
* [Python 3](https://www.python.org/ftp/python/3.7.1/python-3.7.1.exe)
* [Git Bash Terminal](https://git-scm.com/download/win)

### Install required lib
$ `pip install flask`  
$ `pip install functools`  
$ `pip install sqlalchemy`  
$ `pip install httplib2`  
$ `pip install requests`  
$ `pip install oauth2client`  

### How To Run
instde project folder open `git bash` then write  
$ `python add_items.py`  
$ `python views.py`  

## Preview (ScreenShot)

Store Page
![Store Page](screenshot/Store_Page.png)

Product Page
http://localhost:8000/store/(StoreName)/products
![Product Page](screenshot/Products_Page.png)

Login Page
http://localhost:8000/login
![Login Page](screenshot/Login_Page.png)

Users Page
http://localhost:8000/users
![Users Page](screenshot/Users_Page.png)

Create New Store Page
http://localhost:8000/
![Create New Store Page](screenshot/New_Store_Page.png)

Edit Store Page
http://localhost:8000/store/(StoreName)/edit
![Edit Store Page](screenshot/Edit_Store_Page.png)

Delete Store Page
http://localhost:8000/store/(StoreName)/delete
![Delete Store Page](screenshot/Delete_Store_Page.png)

Create New product Page
http://localhost:8000/store/(StoreName)/product/new
![Create New product Page](screenshot/New_Product_Page.png)

Edit product Page
http://localhost:8000/store/(StoreName)/(ProductName)/edit
![Edit product Page](screenshot/Edit_Product_Page.png)

Delete product Page
http://localhost:8000/store/(StoreName)/(ProductName)/delete
![Delete product Page](screenshot/Delete_Product_Page.png)

JSON Endpoint
http://localhost:8000/stores/json
![JSON Endpoint](screenshot/stores_json.png)

http://localhost:8000/store/Carfoure/products/json
![JSON Endpoint](screenshot/Carfoure_products_json.png)

http://localhost:8000/store/Carfoure/product/Tomato/json
![JSON Endpoint](screenshot/Carfoure_product_Tomato_json.png)
