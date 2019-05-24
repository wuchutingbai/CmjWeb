# 路由正则匹配改造
from wsgiref.simple_server import make_server
from webob import Request, Response, exc
from webob.dec import wsgify
import re


#  正则匹配
class Application:
    ROUTETABLE = []  # 有序列表便于路由的正则匹配的顺序

    @classmethod
    def register(cls, pattern):
        def wrapper(handler):
            cls.ROUTETABLE.append((re.compile(pattern), handler))
            return handler  # 思考：可以不把handler return 出来吗？
        return wrapper

    @wsgify
    def __call__(self, request: Request) -> Response:
        for pattern, handler in self.ROUTETABLE:
            if pattern.match(request.path):
                return handler(request)
        raise exc.HTTPNotFound('<h1>你访问的页面被外星人劫持了</h1>')


@Application.register('^/$')
def index(request: Request) -> Response:
    res = Response()
    res.status_code = 200
    res.content_type = 'text/html'
    res.charset = 'utf=8'
    res.body = '<h1>welcome to cmjwebzsz</h1>'.encode()
    return res


@Application.register('^/python$')
def show_python(request: Request) -> Response:
    res = Response()
    res.content_type = 'test/plain'
    res.charset = 'utf-8'
    res.body = '<h1>welcome to python</h1>'.encode()
    return res


if __name__ == '__main__':

    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip, port, Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


