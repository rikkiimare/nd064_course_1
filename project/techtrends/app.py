# SQLlite import
# Another comment
import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
from datetime import datetime
import sys

# Global variable
connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global connection_count
    connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
#       log_msg('None existing article accessed - 404 returned')
        logger.error('"{id}" NOT FOUND - ERROR 404'.format(id=post_id))
        return render_template('404.html'), 404
    else:
        logger.info('Article "{title}" retrieved'.format(title=post['title']))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info('Access "About Us" page')
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logger.info('New article "{titled}" added'.format(titled=title))
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the metrics functionality
@app.route('/metrics')
def metrics():
    cnct = get_db_connection()
    posts = cnct.execute('SELECT * FROM posts').fetchall()
    cnct.close()
    post_cnt = len(posts)
    data = {"db_connection_count": connection_count, "post_count": post_cnt}
    return data

# Define the health check functionality
@app.route('/healthz')
def healthz():
    response = app.response_class(
        response = json.dumps({"result":"OK - healthy"}),
        status = 200,
        mimetype = 'application/json'
    )
    # app.logger.info('healthz status request successful')
    logger.info('healthz status request successful')
    return response

# Add messages to the Log
#def log_msg(msg):
#    app.logger.info('{time}', '{message}'.format(time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), message=msg))

# start the application on port 3111
if __name__ == "__main__":
    # Stream logs to a file, and set the default log level to DEBUG

    # file, stdout & stderr handlers
    file_handler = logging.FileHandler("app.log")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [file_handler, stdout_handler, stderr_handler]

    # basicConfig
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
                        handlers=handlers)
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    app.run(host='0.0.0.0', port='3111')
