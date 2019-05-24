from wsgiref.simple_server import make_server
from webob import Request, Response, exc
from webob.dec import wsgify


class Application:
    ROUTETABLE = {}

    @classmethod
    def register(cls, path):
        def wrapper(handler):
            cls.ROUTETABLE[path] = handler
            return handler  # 思考：可以不把handler return 出来吗？
        return wrapper

    @wsgify
    def __call__(self, request: Request) -> Response:
        try:
            return self.ROUTETABLE[request.path](request)
        except Exception as e:
            raise exc.HTTPNotFound('<h1>你访问的页面被外星人劫持了</h1>')  #使用自带webob自带的notfound


@Application.register('/')
def index(request: Request) -> Response:
    res = Response()
    res.status_code = 200
    res.content_type = 'text/html'
    res.charset = 'utf=8'
    res.body = '<h1>welcome to cmjwebzzz</h1>'.encode()
    return res


@Application.register('/python')
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

# 这样一个router的基本功能就实现了，后面我们需要路由正则匹配以及Request.method的路径过滤