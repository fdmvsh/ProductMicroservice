# Product aggregator microservice

## Prerequisites

Docker

	or

Python 3

Redis

MySQL

## Installing

Run:
```
git clone https://github.com/fdmvsh/ProductMicroservice/
python3 -m venv env
source env/bin/activate
pip install --no-cache-dir -r requirements.txt
export SQLALCHEMY_DATABASE_URI= # connection string to your MySQL database, e.g. "mysql+pymysql://user:password@localhost:3306/DB", SQLite or any other SQLAlchemy supported database (connector installation needed if not MySQL/SQLite)
export OFFERS_MS= # path to the Offers microservice
python3 micro.py
```
Background service (assuming Redis is reachable at redis://localhost:6379/0):
```
celery -A bgjob worker
```
```
celery -A bgjob beat
```

### Docker

Run:
```
docker-compose up
```

## Documentation

Base URL​:​ http://localhost:5000/api/v1

### GET /products
```
Response:
200 OK
[
	{
		“id”: 42,
		“name”: 1000,
		“description”: 5
	}
]
```

### GET /products/:id:
```
Response:
200 OK
[
{
		“id”: 42,
		“name”: 1000,
		“description”: 5
	}
]
404 NOT FOUND
{
	“code”: “NOT FOUND”,
	“msg”: <message>
}
```

### POST /products
```
Request:
{
	“name”: “Benzinová sekačka Dosquarna”,
	“description: “Nejlepší sekačka na trhu. TLDR”
}
Response:
201 CREATED
{
	“id”: 42
}
400 BAD REQUEST
{
	“code”: “BAD_REQUEST”,
	“msg”: <message>
}
```

### PUT /products/:id:
```
Request:
id in path;
{
	“name”: “Benzinová sekačka Dosquarna”,
	“description: “Nejlepší sekačka na trhu. TLDR”
}
Response:
{
	“name”: “Benzinová sekačka Dosquarna”,
	“description: “Nejlepší sekačka na trhu. TLDR”
}
404 NOT FOUND
{
	“code”: “NOT FOUND”,
	“msg”: <message>
}
```

### DELETE /products/:id:
```
Request:
id in path
Response:
{
	“Result”: True
}
404 NOT FOUND
{
	“code”: “NOT FOUND”,
	“msg”: <message>
}
```

## Running the tests

Run:

```
pytest
```

## Built with

* [Flask](https://palletsprojects.com/p/flask/) - a micro web framework
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and object relational mapper
* [Celery](http://www.celeryproject.org/) - distributed task queue
* [Requests](https://requests.readthedocs.io/en/master/) - HTTP library

## License

This project is licensed under the WTFPL License.
