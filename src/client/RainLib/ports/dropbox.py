from __future__ import absolute_import
import webbrowser
import BaseHTTPServer
from dropbox.client import DropboxOAuth2Flow, DropboxClient
import urllib
from .. import clouddrive

__name__ = 'DropBox'


class DropBox(clouddrive.CloudDrive):
    name = "DropBox"

    def __init__(self, access_token):
            self.client = DropboxClient(access_token)
            self.access_token = access_token
            clouddrive.CloudDrive.__init__(self, access_token)

    @staticmethod
    def auth():
        app_key = 'knbyx2adg14kkn5'
        app_secret = 'kh3ulgqry8jffqp'
        global Auth_DROPMytoken
        global Auth_Drop_Running_true

        def keep_running():
            global Auth_Drop_Running_true
            return Auth_Drop_Running_true

        class AuthHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_HEAD(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()

            def do_GET(s):
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                if s.path.find("code=") != -1:
                    global Auth_DROPMytoken
                    global Auth_Drop_Running_true
                    Auth_DROPMytoken = s.path
                    Auth_Drop_Running_true = False
                    s.wfile.write("ok see command line")
                    return

        class MYrequest:

            def __init__(self, url):
                self.url = url

            def get(self, mystring):
                if self.url.find(mystring) == -1:
                    return
                item = self.url.split(mystring + "=")[1]
                if item.find("&") != -1:
                    item = item.split("&")[0]
                return urllib.unquote(item).decode()


        redirect_url = "http://localhost:8080"
        my_session = {}
        Auth_Drop_Running_true = True
        flow = DropboxOAuth2Flow(app_key, app_secret, redirect_url, my_session, "dropbox-auth-csrf-token")

        authorize_url = flow.start()
        webbrowser.open(authorize_url)

        try:
            httpd = BaseHTTPServer.HTTPServer(("", 8080), AuthHandler)
            while keep_running():
                httpd.handle_request()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

        token, user_id, url_state = flow.finish(MYrequest(Auth_DROPMytoken))
        clouddrive.CloudDrive.access_token = token
        return token


    def read(self, filename):
        try:
            f = open(filename, 'rb', overwrite)
            response = self.client.put_file(filename, f)
            f.close()
        except:
            return -1
        return 1

    def write(self, filename):
        try:
            out = open("/tmp" + filename, 'wb')
            with self.client.get_file(remote_file) as f:
                out.write(f.read())
            out.close()
        except:
            return -1
        return 1

    def mkdir(self, dirname):
        try:
            self.client.file_create_folder(dirname)
        except:
            return -1
        return 1

    def delete(self, filename):
        try:
            self.client.file_delete(filename)
        except:
            return -1
        return 1
    

