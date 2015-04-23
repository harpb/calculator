# Calculator
An angular based front-end implementation of basic calculator with a Django api. 

# Getting Started

0. Create a virtual environment and install python dependencies:
	
	```bash
	$ pip install -r requirements.txt
	```

0. Start django webserver:
	
	```bash
	$ cd webapp
	$ ./manage.py runserver
	```

0. Play webapp @ [`/static/calculator/calculator_index.html`](http://127.0.0.1:8000/static/calculator/calculator_index.html)

# Architecture

0. `webapp/static/calculator/calculator_index.jade` is the HTML entry point. It uses `ng-app='app'` to start the angular app and `calculator` is a directive with the business logic. 

0. The game logic is written in the back-end. `calculator` directive calls the REST API endpoint `/calculator/evaluate/` to get the next answer. Based on the response, the UI is updated to reflect the response from the back-end. 

0. The game logic is in `webapp/calculator/models.py`, more specifically `def evaluate(cls, expression):)`.