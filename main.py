"""
Сокращатель ссылок

API:
 - GET /?url=https://www.domain.com/foo/bar?spam=eggs
   http://d.ssl2.ru/iOkfe

 - GET /iOkfe
   HTTP 301 https://www.domain.com/foo/bar?spam=eggs

"""
import os
import random
import shelve
import string

from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import redirect, text


MAX_LENGTH = 5
DB_FILENAME = 'db'

app = Sanic()


def gen_short():
    return ''.join(random.choices(string.ascii_letters, k=MAX_LENGTH))


def add_url(url, *, db):
    short = gen_short()
    while short in db:
        short = gen_short()

    db[short] = url
    return short


def get_url(short, *, db):
    return db.get(short)


@app.route('/')
async def add(request):
    short = ''

    if request.args.get('url'):
        short = add_url(request.args['url'][0], db=request.app.db)

    return text(short)


@app.route('/<short>')
async def get(request, short):
    url = get_url(short, db=request.app.db)
    if not url:
        abort(404, 'Url not found')

    return redirect(url, status=301)


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = shelve.open(DB_FILENAME)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
