from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser
class GetHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = "text/html"
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = "image/jpg"
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = "image/gif"
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = "application/javascript"
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = "text/css"
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                self.wfile.write(bytes(file_to_open, "utf-8"))
            return

        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)
    
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes('Client: %s\n' % str(self.client_address), "utf-8"))
        self.wfile.write(bytes('User-agent: %s\n' % str(self.headers['user-agent']), "utf-8"))
        self.wfile.write(bytes('Path: %s\n' % self.path, "utf-8"))
        self.wfile.write(bytes('Form data:\n', "utf-8"))

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write(bytes('\tUploaded %s as "%s" (%d bytes)\n' % (field, field_item.filename, file_len), "utf-8"))
            else:
                # Regular form value
                self.wfile.write(bytes('\t%s=%s\n' % (field, form[field].value), "utf-8"))
                print('%s\n' % (form[field].value))
        return



if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', PORT_NUMBER), GetHandler)
    print ('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()