#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import atexit
import base64
import cgi
import logging
import json
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageCms

from http.server import BaseHTTPRequestHandler, HTTPServer

from style_transfer import *

def prof_to_prof(image, src_prof, dst_prof, **kwargs):
    src_prof = io.BytesIO(src_prof)
    dst_prof = io.BytesIO(dst_prof)
    return ImageCms.profileToProfile(image, src_prof, dst_prof, **kwargs)


def load_image(path, proof_prof=None):
    srgb_profile = (Path(__file__).resolve().parent / 'sRGB Profile.icc').read_bytes()
    src_prof = dst_prof = srgb_profile
    try:
        image = Image.open(path)
        if 'icc_profile' in image.info:
            src_prof = image.info['icc_profile']
        else:
            image = image.convert('RGB')
        if proof_prof is None:
            if src_prof == dst_prof:
                return image.convert('RGB')
            return prof_to_prof(image, src_prof, dst_prof, outputMode='RGB')
        proof_prof = Path(proof_prof).read_bytes()
        cmyk = prof_to_prof(image, src_prof, proof_prof, outputMode='CMYK')
        return prof_to_prof(cmyk, proof_prof, dst_prof, outputMode='RGB')
    except OSError as err:
        print_error(err)
        sys.exit(1)


class S(BaseHTTPRequestHandler):

    #-------------------------------- ROBERTO -------------------------
    def processImage(self, img, idNft):
        st_model = StyleTransfer()

        content_img = img
        style_img = load_image(f"nft/{idNft}.jpeg")

        image_type = "pil"
        callback = Callback(st_model, image_type=image_type)
        atexit.register(callback.close)

        st_model.stylize(content_img, [style_img], end_scale=128, callback=callback)
        output_img = st_model.get_image()
        return output_img

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
