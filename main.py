"""
Сокращатель ссылок
"""
from concurrent.futures import ThreadPoolExecutor
import os
import random
import shelve
import string

from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import redirect, text


SITENAME = os.getenv('SITENAME', 'http://127.0.0.1:8080')
MAX_LENGTH = 5
BASE_DIR = os.path.abspath('.')
DB_PATH = os.path.join(BASE_DIR, 'data', 'db')

app = Sanic()


def generate_slug():
    return ''.join(random.choices(string.ascii_letters, k=MAX_LENGTH))


def add_url(url, *, db):
    slug = generate_slug()
    while slug in db:
        slug = generate_slug()

    db[slug] = url
    return slug


@app.route('/')
async def add(request):
    if not request.args.get('url'):
        abort(400, "Missing 'url' parameter")

    fut = request.app.executor.submit(add_url, request.args['url'][0], db=request.app.db)
    slug = fut.result()
    return text(f'{SITENAME}/{slug}')


@app.route('/<slug>')
async def get(request, slug):
    url = request.app.db.get(slug)
    if not url:
        abort(404, 'Url not found')

    return redirect(url, status=301)


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = shelve.open(DB_PATH)

    # Многопоточный executor для неблокирующей записи в shelve
    app.executor = ThreadPoolExecutor()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
