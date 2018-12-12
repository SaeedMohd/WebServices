# web.wsgi
#!/usr/bin/python
import sys

#Expand Python classes path with your app's path
sys.path.insert(0, "/var/www/Inspection/WebServices/")

from WebServices import app

#Put logging code (and imports) here ...
#Initialize WSGI app object
application = app