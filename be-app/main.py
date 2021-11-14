#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import cgi
from PIL import Image
from io import BytesIO
import base64


class S(BaseHTTPRequestHandler):
    
    #-------------------------------- ROBERTO -------------------------
    def processImage(self, img, idNft):
        return img
    #-------------------------------- ROBERTO -------------------------

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        
        obj = json.loads(post_data)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        
        if (self.path == '/process-image'):
            img = Image.open(BytesIO(base64.b64decode(obj['img'])))
            processedImage = self.processImage(img, obj['id'])
            buffered = BytesIO()
            processedImage.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            out = {
                'processed': obj['img']
            }

            self._set_response()
            self.wfile.write(json.dumps(out).encode())
    
    def do_OPTIONS(self):
        self._set_response()

def run(server_class=HTTPServer, handler_class=S, port=3000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd at port '+str(port)+'...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

        
