from gevent import monkey; monkey.patch_all()
import logging
log = logging.getLogger(__name__)

import os
import traceback
import sys
from gevent.pywsgi import WSGIServer

from django.core.wsgi import get_wsgi_application
from django.core.signals import got_request_exception

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

def exception_printer(sender, **kwargs):
    traceback.print_exc()
got_request_exception.connect(exception_printer)

PORT = 8001
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

print 'Serving on %d...' % PORT
WSGIServer(('', PORT), get_wsgi_application(), backlog = 4096).serve_forever()
