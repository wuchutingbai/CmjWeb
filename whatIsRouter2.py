# router进一步实现
from wsgiref.simple_server import make_server
from webob import Request, Response
from webob.dec import wsgify


def index(request: Request):
    res = Response()
    res.status_code = 200
    res.content_type = 'text/html'
    res.charset = 'utf=8'
    res.body = '<h1>welcome to cmjweb</h1>'.encode()
    return res


def show_python(request: Request):
    res = Response()
    res.content_type = 'test/plain'
    res.charset = 'utf-8'
    res.body = '<h1>welcome to python</h1>'.encode()
    return res


def notfound(request: Request):
    res = Response()
    res.status_code = 404
    res.body = '<h1>你访问的页面被外星人劫持了</h1>'.encode()
    return res


route_table = {
    '/': index,
    '/python': show_python,
}


@wsgify
def app(request: Request):
    print(request.method)
    print(request.path)
    print(request.query_string)
    print(request.GET)
    print(request.Post)
    print("params = {}".format(request.params))

    return route_table.get(request.path, notfound)(request)


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip, port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

#这个方法能实现路由,那么我们能不能实现动态的修改路由的配置呢？请参考whatIsRouter3