from wsgiref.simple_server import make_server
from webob import Request, Response
from webob.dec import wsgify


def index(request: Request) -> Response:
    res = Response()
    res.status_code = 200
    res.content_type = 'text/html'
    res.charset = 'utf=8'
    res.body = '<h1>welcome to cmjweb</h1>'.encode()
    return res


def show_python(request: Request) -> Response:
    res = Response()
    res.content_type = 'test/plain'
    res.charset = 'utf-8'
    res.body = '<h1>welcome to python</h1>'.encode()
    return res

# wsgi的接口传入的必须是可调用对象。利用__call__将类包装成可调用对象


class Application:  # wsgi的接口传入的必须是可调用对象。利用__call__将类包装成可调用对象
    ROUTERTABLE = {}
    @classmethod
    def register(cls, path, handler):
        cls.ROUTERTABLE[path] = handler

    def notfound(self, request:Request) -> Response:
        res = Response()
        res.status_code = 404
        res.body = '<h1>你访问的页面被外星人劫持了</h1>'.encode()
        return res

    @wsgify
    def __call__(self, request:Request) -> Response:
        return self.ROUTERTABLE.get(request.path, self.notfound)(request)


if __name__ == '__main__':
    Application.register('/', index)
    Application.register('/python', show_python)

    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip, port, Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

#我们需要进一步对router优化，将注册函数改成装饰器

