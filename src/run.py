from app import app

__author__ = 'cfloryiv'

app.run(debug=app.config['DEBUG'], port=5000)
