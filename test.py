# 本框架是使用wsgi接口实现

from wsgiref.simple_server import make_server, demo_app


def app(environ, start_response):
    pathinfo = environ.get('PATH_INFO')
    qstr = environ.get("QUERY_STRING")
    print(pathinfo)
    print(qstr)
    print('hello')
    status = '200 OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    start_response(status, headers)  # 通过这个函数在凑表头
    html = '<h1>cmjweb aaa</h1>'.encode("utf-8")  # 返回的必须是byte并且可迭代
    return [html]


ip = '127.0.0.1'
port = 9999
server = make_server(ip, port, app)
server.serve_forever()
