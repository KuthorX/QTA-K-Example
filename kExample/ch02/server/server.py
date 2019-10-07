# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from cgi import parse_header, parse_multipart
import json

host = ('localhost', 1996)


class Request(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        input: a, b
        output: a + b
        e.g. curl -v "http://localhost:1996?a=1&b=2"
             return 3
        """
        get_dict = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
        try:
            a = get_dict["a"]
            b = get_dict["b"]
            c = int(a) + int(b)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write(str(c).encode())
        except Exception as err:
            print(err)
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write("".encode())
        return

    def do_POST(self):
        """
        input: x, y
        output: x * y
        e.g. curl -v "http://localhost:1996" -d "{\"x\": 1, \"y\": 2}" -H "Content-Type: application/json"
             return 2
        """
        content_type, p_dict = parse_header(self.headers['content-type'])
        if content_type == 'multipart/form-data':
            post_dict = parse_multipart(self.rfile, p_dict)
        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_dict = parse.parse_qs(
                self.rfile.read(length),
                keep_blank_values=1)
        elif content_type == 'application/json':
            content_length = int(self.headers['Content-Length'])
            post_dict = json.loads(self.rfile.read(content_length))
        else:
            post_dict = {}
        print(post_dict)
        try:
            x = post_dict["x"]
            y = post_dict["y"]
            z = int(x) * int(y)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write(str(z).encode())
        except Exception as err:
            print("aa")
            print(err)
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write("".encode())
        return


if __name__ == '__main__':
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
