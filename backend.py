# Flask server for NTC Bot

from flask import Flask # import flask

app = Flask(__name__) # make it easier to use flask

# start the route of the website
@app.route('/')
def home():
    return 'Loaded Site'

# run it
if __name__ == '__main__':
    app.run(debug=True)
