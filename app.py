#!/usr/bin/env python3

import os

from flask import Flask, render_template, redirect, url_for, request, send_file
from db import setup_db, get_db
from memer import make_meme
from io import BytesIO

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = bool(os.environ.get('FLASK_DEBUG', 1))
setup_db(app)

@app.route('/add_meme', methods=['POST'])
def add_meme():
    bg_url = request.form['image']
    top_caption = request.form['top_caption']
    bottom_caption = request.form['bottom_caption']

    get_db().execute('INSERT INTO memes(url, caption1, caption2, image) VALUES(?, ?, ?, ?);', (
        bg_url,
        top_caption,
        bottom_caption,
        make_meme(bg_url, top_caption, bottom_caption).getvalue()
    ))

    return redirect(url_for('index'))

@app.route('/meme/<id>')
def show(id):
    meme = get_db().select('SELECT id, url, caption1, caption2 FROM memes WHERE id=?;',
                           [id])[0]

    return render_template('show.html', meme=meme)

@app.route('/meme/<id>.jpg')
def show_image(id):
    memes = get_db().select('SELECT id, url, caption1, caption2, image FROM memes WHERE id = ?', [int(id)])
    meme = memes[0]

    print('meme')
    image = BytesIO(meme['image'])
    return send_file(image, mimetype='image/jpeg')


@app.route('/meme_form')
def meme_form():
    return render_template('meme-form.html')

@app.route('/')
def index():
    memes = get_db().select('SELECT id, url, caption1, caption2 FROM memes')
    return render_template('homepage.html', memes=memes)

if __name__ == '__main__':
    app.run(host=os.environ.get('BIND_TO', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=bool(int(os.environ.get('FLASK_DEBUG', 1))))
