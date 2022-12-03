from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            ...
            # test that you're getting a template
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- ultimately,', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games
            #       (imported from app.py above)

            response = client.post("/api/new-game")
            json_response = response.get_json()

            # actually good use case for bracket notaion; sometimes want to 
            # raise an error
            game_id = json_response.get("gameId")
            board = json_response.get("board")

            self.assertTrue(isinstance(game_id, str))
            self.assertTrue(isinstance(board, list))
            # can also check if first element of board is also a list; we want to
            # make sure we have a list of lists
            self.assertTrue(game_id in games) # can use assertIn (a bit more explicit)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}

            response = client.post('/api/new-game')
            json_response = response.get_json()
            game_id = json_response.get('gameId')
            curr_game = games.get(game_id)
            curr_game.board = [
                ['B','E','E','T','V'],
                ['M','M','M','M','M'],
                ['M','M','M','M','M'],
                ['M','M','M','M','M'],
                ['M','M','M','M','M']
            ]

            # good test
            # simulating a client-side post request to the API
            # client sends JSON, response is JSON from API
            # (reponse sent to client-side would be a JS obj)
            response = client.post(
                '/api/score-word', 
                json={"game_id":game_id, "word":"BEET"}
            )
            # json_response now holds a python dictionary
            json_response = response.get_json()
            # now we can compare json_reponse (dict) to a dicitonary-literal
            self.assertEqual(json_response, {"result": "ok"})


            # bad test - word not on board
            response = client.post(
                '/api/score-word', 
                json={"game_id":game_id, "word":"CAT"}
            )
            json_response = response.get_json()
            self.assertEqual(json_response, {"result": "not-on-board"})


            # bad test - word not a word
            response = client.post(
                '/api/score-word', 
                json={"game_id":game_id, "word":"GLDFKJGH!!"}
            )
            json_response = response.get_json()
            self.assertEqual(json_response, {"result": "not-word"})


