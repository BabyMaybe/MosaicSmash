import os

DEBUG = True

# Use this for local development on OSX
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join('/Users/eric_varela/git/MosaicSmash', 'db.sqlite3'),
   }
}

## Development SECRET_KEY
SECRET_KEY = '''7!cx=#222y$ty_bc(ap*$-f%3+vp5n4u#x7ys0hwe8z@q*e1vd'''
