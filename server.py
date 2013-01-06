from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
from jinja2 import Environment, FileSystemLoader
import os
from os import curdir, sep

class RequestHandler(BaseHTTPRequestHandler):
    ''' Handler for HTTP requests. '''


    def send_200_response_headers(self, content_type):
        ''' Send an OK response with the correct content type. '''

        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def render_main_template(self, env, page_content, title):
        ''' Render the main template with specified content and title. '''

        main = env.get_template('main_template.html')
        self.wfile.write(main.render(page_content = page_content, title = title))

    def do_GET(self):
        try:

            # Let the Jinja environment know that the templates folder is where
            # the templates should be found.
            env = Environment(loader = FileSystemLoader('templates'))

            #
            # Handle static css / javascript requests.
            #
            if self.path.endswith('.css') or self.path.endswith('.js'):
                f = open(curdir + sep + self.path)

                # Only difference between the two is the type of response in the
                # headers.
                if self.path.endswith('.css'):
                    self.send_200_response_headers('text/css')
                if self.path.endswith('.js'):
                    self.send_200_response_headers('text/javascript')

                self.wfile.write(f.read())
                f.close()
                return

            # TODO: refactor all of this to be based on path, not just file ending

            #
            # Handle static json requests for recipes
            #
            if self.path.endswith('.json'):
                f = open(curdir + sep + 'recipes' + sep + self.path)

                self.send_200_response_headers('text/json')

                self.wfile.write(f.read())
                f.close()
                return

            #
            # Handle generic requests for the index page
            #
            if self.path == '' or self.path == '/':
                self.send_200_response_headers('text/html')

                # Send a list of recipe titles and their associated urls for rendering
                recipes = []
                dirList = os.listdir(curdir + sep + "recipes")
                for fname in dirList:
                    url = fname[:-5]
                    title = url.replace("-", " ").title()
                    recipes += [{'url': url, 'title': title}]

                page_content = env.get_template('frontpage.html')
                page_content = page_content.render(recipes = recipes)
                self.render_main_template(env, page_content, "Recipe List")
                return

            #
            # All remaining requests should be for hosted recipes.
            #

            # Remove final slashes
            file_requested = self.path
            if file_requested[-1] == '/':
                file_requested = file_requested[:-1]

            # Can only handle serving recipes for now
            path_to_file = curdir + sep + 'recipes' + sep + file_requested + '.json'

            f = open(path_to_file)
            recipe = json.loads(f.read())

            self.send_200_response_headers('text/html')
            page_content = env.get_template('recipe.html')
            page_content = page_content.render(recipe = recipe)
            self.render_main_template(env, page_content, "Recipe:" + recipe['title'])

        except IOError:
            ''' A generic IO error means the file does not exist. '''
            self.send_error(404,'File Not Found: %s' % self.path)

    # def do_POST(self):
    #     global rootnode
    #     try:
    #         ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    #         if ctype == 'multipart/form-data':
    #             query=cgi.parse_multipart(self.rfile, pdict)
    #         self.send_response(301)

    #         self.end_headers()
    #         upfilecontent = query.get('upfile')
    #         print "filecontent", upfilecontent[0]
    #         self.wfile.write("<HTML>POST OK.<BR><BR>");
    #         self.wfile.write(upfilecontent[0]);
    #     except :
    #         pass

def main():
    ''' Start the http server. '''

    try:
        server = HTTPServer(('', 80), RequestHandler)
        print 'Starting server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Server recieved request to shut down'
        server.socket.close()

if __name__ == '__main__':
    main()