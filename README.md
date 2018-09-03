# clckclck

clckclck - прототип сокращателя ссылок. Коротка ссылка генерируется рандомом, в качестве БД используется стандартная библиотека shelve.

## API

```
> GET /?url=https://www.domain.com/foo/bar?spam=eggs

http://c.ssl2.ru/iOkfe
```

```
> GET /iOkfe

HTTP 301 https://www.domain.com/foo/bar?spam=eggs
```

## Деплой

```
$ docker run -d --name clckclck \
    -p 80:8080 \
    -v `pwd`/data:/app/data \
    -e SITENAME=http://c.ssl2.ru \
    rschweppes/clckclck:latest
```

## Бенчмарки

1 CPU, 512 MB RAM, SSD

```
$ wrk -c100 -t12 -d10s "http://c.ssl2.ru/?url=https://stackoverflow.com/"
Running 10s test @ http://c.ssl2.ru/?url=https://stackoverflow.com/
  12 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    56.25ms    4.79ms 109.97ms   93.01%
    Req/Sec   142.08     31.74   161.00     79.75%
  17005 requests in 10.03s, 2.29MB read
Requests/sec:   1694.97
Transfer/sec:    233.39KB
```

## Используемые технологии

- Python - хорошо подходит для прототипирования;
- shelve - простое хранилище;
- [sanic](https://github.com/channelcat/sanic) - быстрый асинхронный веб-сервер.

## На будущее

- Использовать внешнее многопоточное key-value или документное хранилище, потому что текущее решение не масштабируемое (shelve можно открыть только в одном процессе).
- При больших объёмах данных проверка коллизий может занимать длительное время (`while slug in db: slug = generate_slug()`). Нужно подумать о том, чтобы генерировать ссылки не рандомом, а от последней сгенерированной (`aaaaa`, `aaaab`, `aaaac`).
- Использовать nginx в качестве реверс-прокси, настроить rate limiting.
