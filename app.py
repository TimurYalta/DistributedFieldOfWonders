from flask import Flask, request
import Pyro4
import random

app = Flask(__name__)

users = {}
questions = {'Each modern man knows what is \"I don\'t understand you\" in a language of Australian aborigens': 'Kangaroo'}

@app.route('/registerUser')
def register_user():
    uri = request.get_json()['uri']
    users[len(users) + 1] = uri
    if len(users) == 5:
        start_game()

def start_game():
    question = random.choice(questions.keys())
    answer = questions[question]
    hashed_letters = [hash(letter) for letter in answer]
    hashed_answer = hash(answer)
    for uri in users.values():
        start_game_marker = Pyro4.Proxy(uri)
        start_game_marker.start_game(users, question, hashed_letters, hashed_answer)
    users.clear()

if __name__ == '__main__':
    app.run()
