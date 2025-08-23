#!/usr/bin/env python
import os
import sys
import django
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# Setup Django
django.setup()

# Now import Django-dependent modules
from django.conf import settings
from chat.tornado.http_handler import HttpHandler
from chat.tornado.static_file_handler import PychatStaticFileHandler
from chat.tornado.tornado_handler import TornadoHandler

def main():
    port = 8888
    host = '0.0.0.0'
    
    application = Application([
        (r'/api/.*', HttpHandler),
        (r'/photo/(.*)', PychatStaticFileHandler, {'path': settings.MEDIA_ROOT}),
        (r'/ws', TornadoHandler),
    ], debug=settings.DEBUG, default_host=host)
    
    http_server = HTTPServer(application, max_buffer_size=1000000000)  # 1GB
    http_server.bind(port, host)
    http_server.start(1)
    
    print(f'Tornado server started at {host}:{port}')
    print('Press Ctrl+C to stop')
    
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        print('\nShutting down...')
        IOLoop.current().stop()

if __name__ == '__main__':
    main()