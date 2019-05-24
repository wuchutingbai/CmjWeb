# 路由最简单的实现
from wsgiref.simple_server import make_server
from webob import Request, Response
from webob.dec import wsgify


@wsgify
def app(request: Request):
    print(request.method)
    print(request.path)
    print(request.query_string)
    print(request.GET)
    print(request.Post)
    print("params = {}".format(request.params))

    res = Response()
    if request.path == "/":
        res.status_code = 200
        res.content_type = 'text/html'
        res.charset = 'utf=8'
        res.body = '<h1>welcome to cmjweb</h1>'.encode()
    elif request.path == '/python':
        res.content_type = 'test/plain'
        res.charset = 'utf-8'
        res.body = '<h1>welcome to python</h1>'.encode()
    else:
        res.status_code = 404
        res.body = '<h1>你访问的页面被外星人劫持了</h1>'.encode()
    return res


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip, port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


#  很明显，这个方法虽然解决了路由的问题，但是逻辑写死了，不方便重用。请参照whatIsRouter的方法改进
