from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    # breakpoint()

    # UPDATE TO "jsonify()"
    return {
        "gameId": game_id,
        "board": game.board
    }

# this API receives JSON from client
@app.post("/api/score-word")
def score_word():
    """score post'd word; return if valid or reason not"""

    # request_data is a dictionary, parsed from .json
    request_data = request.json
    game_id = request_data["game_id"]
    game = games[game_id]

    if game.is_word_in_word_list(request_data["word"]):
        if game.check_word_on_board(request_data["word"]):
            # jsonify will take any kwargs passed into it
            # and creates a dictionary and turns it to JSON
            return jsonify(result="ok")
        else:
            return jsonify(result="not-on-board")
    else:
        return jsonify(result="not-word")





