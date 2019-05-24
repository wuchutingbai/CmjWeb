# 让一个url支持多个method
from wsgiref.simple_server import make_server
from webob import Request, Response, exc
from webob.dec import wsgify
import re



class Application:
    ROUTETABLE = []  # 有序列表便于路由的正则匹配的顺序

    @classmethod
    def route(cls, pattern, *methods):  # 将methods放到后面做可变参数
        def wrapper(handler):
            cls.ROUTETABLE.append((methods, re.compile(pattern), handler))
            return handler  # 思考：可以不把handler return 出来吗？
        return wrapper

    @classmethod
    def get(cls, pattern):
        return cls.route('GET', pattern)

    @classmethod
    def post(cls, pattern):
        return cls.route('POST', pattern)

    @classmethod
    def head(cls, pattern):
        return cls.route('HEAD', pattern)

    @wsgify
    def __call__(self, request: Request) -> Response:
        print(self.ROUTETABLE)
        for methods, pattern, handler in self.ROUTETABLE:
            # 如果注册路由时候没有写method那么那个handler支持所有的请求方法
            if not methods or request.method.upper() in methods:
                if pattern.match(request.path):
                    return handler(request)
        raise exc.HTTPNotFound('<h1>你访问的页面被外星人劫持了</h1>')


@Application.get('^/$')
def index(request: Request) -> Response:
    res = Response()
    res.status_code = 200
    res.content_type = 'text/html'
    res.charset = 'utf=8'
    res.body = '<h1>welcome to cmjwebzsz</h1>'.encode()
    return res


@Application.post('^/python$')
def show_python(request: Request) -> Response:
    res = Response()
    res.content_type = 'test/plain'
    res.charset = 'utf-8'
    res.body = '<h1>welcome to python6</h1>'.encode()
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


#  路由的功能到这里就结束了。接下来要是实现的是多级路由和路由分组