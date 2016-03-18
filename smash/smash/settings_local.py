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
SECRET_KEY = '''smashdevq+b8e9_o^al0umgv_kxh&a4y_e5vsx7pl3%r(^%tmpd_&)p4)3smashdev'''
