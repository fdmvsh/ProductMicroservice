import pytest
import requests

url = 'http://127.0.0.1:5000' # The root url of the flask app

def test_index_page():
	r = requests.get(url+'/api/v1/products') # Assumses that it has a path of "/"
	assert r.status_code == 200 # Assumes that it will return a 200 response

def test_product_create():
	global namee, descriptione, idd
	namee = "dsfdsf"
	descriptione = "Need to find a good Python tutorial on the web"
	r = requests.post(url+'/api/v1/products',
			json = {'name': namee,
				'description': descriptione}) # Assumses that it has a path of "/"
	idd = r.json()['id']
	assert r.status_code == 201 # Assumes that it will return a 200 response

def test_product_read():
	r = requests.get(url+'/api/v1/products/'+str(idd))
	assert r.status_code == 200
	assert r.json()['name'] == namee
	assert r.json()['description'] == descriptione

def test_product_all_read():
	r = requests.get(url+'/api/v1/products')
	assert r.status_code == 200
	assert len(r.json()) > 0

def test_product_update():
	namee = "dsf"
	descriptione = "ddsf"
	r = requests.put(url+'/api/v1/products/'+str(idd),
			json = {'name': namee,
				'description': descriptione}) # Assumses that it has a path of "/"
	r = requests.get(url+'/api/v1/products/'+str(idd))
	assert r.status_code == 200 # Assumes that it will return a 200 response
	assert r.json()['name'] == namee
	assert r.json()['description'] == descriptione

def test_product_delete():
	r = requests.delete(url+'/api/v1/products/'+str(idd)) # Assumses that it has a path of "/"
	assert r.status_code == 200 # Assumes that it will return a 200 response
	r = requests.get(url+'/api/v1/products/'+str(idd))
	assert r.status_code == 404