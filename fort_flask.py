import imghdr
import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'fort_flask.db'),
    DEBUG=True,
    SECRET_KEY='jkaskjfjklasjkvneqoiiiobijiovi-030-320jfvjmvmvirn3krnvir3gv',
    UPLOAD_DIR=os.path.join(app.root_path, 'static/uploads'),
    MAX_CONTENT_LENGTH=(16 * 1024 * 1024)
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select id, title, text, upload from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():

    file = request.files['upload']
    if file and imghdr.what(file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    else:
        filename = ''    

    db = get_db()
    db.execute('insert into entries (title, text, upload) values (?, ?, ?)',
        [request.form['title'], request.form['text'], filename])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db = get_db()
    cur = db.execute('select upload from entries where id = ?', (id,)) 
    filename = cur.fetchone()
    if filename:
        os.unlink(app.config['UPLOAD_DIR'] + '/' + filename[0])
    db.execute('delete from entries where id = ?', (id,))
    db.commit()
    flash('Post removed')
    return redirect(url_for('show_entries'))
    
    

'''
database functions
'''
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    app.run()
