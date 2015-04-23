# Tic-Tac-Toe
An angular based front-end implementation of tic-tac-toe with a Django api. 

# Getting Started

0. Create a virtual environment and install django:
	
	```bash
	$ pip install -r requirements.txt
	```

0. Start django webserver:
	
	```bash
	$ cd webapp
	$ ./manage.py runserver
	```

0. Play webapp @ [`http://127.0.0.1:8000/static/tic_tac_toe/tic_tac_toe_index.html`](http://127.0.0.1:8000/static/tic_tac_toe/tic_tac_toe_index.html)

# Architecture

0. `webapp/static/tic_tac_toe/tic_tac_toe_index.jade` is the HTML entry point. It uses `ng-app='app'` to start the angular app and `ticTacToe` is a directive with the business logic. `ticTacToe` board consists of `cell` directive. 

0. The game logic is written in the back-end. `ticTacToe` directive calls the REST API endpoint `/tic_tac_toe/next_move/` to get the next computer move and game's status. Based on the response, the UI is updated to reflect the response from the back-end. 

0. The game logic is in `webapp/tic_tac_toe/models.py`, more specifically `def next_computer_position(self)`, for determining state of the game and the computer's next move.