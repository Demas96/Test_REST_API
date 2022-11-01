
install:
	python -m venv venv
	venv\scripts\pip install Flask Flask-RESTful
	venv\scripts\python createDB.py

run:
	venv\scripts\python main.py




