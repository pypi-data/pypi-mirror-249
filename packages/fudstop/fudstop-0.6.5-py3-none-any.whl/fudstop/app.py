import asyncio
import asyncpg
from flask import Flask, render_template
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__, template_folder='.')
CORS(app)  # Enable CORS

# Database connection parameters (as an example, replace with actual credentials)
db_config = {
    'user': 'postgres',
    'password': 'fud',
    'database': 'polygon',
    'host': '127.0.0.1',
    'port': 5432
}
import random

@app.route('/trial')
def trials():
    return render_template('trial.html')



@app.route('/channels')
def channels():
    return render_template('channels.html')
if __name__ == '__main__':
    app.run(debug=True)