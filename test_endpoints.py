import pytest
import requests

url = 'http://127.0.0.1:5000'


def test_product_create():
	global pname, pdescription, pid
	pname = "Example product"
	pdescription = "Example description"
	r = requests.post(url + '/api/v1/products',
			json = {'name': pname,
				'description': pdescription})
	pid = r.json()['id']
	assert r.status_code == 201

def test_product_read():
	r = requests.get(url + '/api/v1/products/' + str(pid))
	assert r.status_code == 200
	assert r.json()['name'] == pname
	assert r.json()['description'] == pdescription

def test_product_all_read():
	r = requests.get(url + '/api/v1/products')
	assert r.status_code == 200
	assert len(r.json()) > 0

def test_product_update():
	pname = "PUT examplename"
	pdescriptione = "PUT exampledesc"
	r = requests.put(url + '/api/v1/products/' + str(pid),
			json = {'name': pname,
				'description': pdescription})
	r = requests.get(url + '/api/v1/products/' + str(pid))
	assert r.status_code == 200
	assert r.json()['name'] == pname
	assert r.json()['description'] == pdescription

def test_product_delete():
	r = requests.delete(url + '/api/v1/products/'+str(pid))
	assert r.status_code == 200
	r = requests.get(url + '/api/v1/products/' + str(pid))
	assert r.status_code == 404
