from tamarcado.settings.base import *


ALLOWED_HOSTS = ['*']
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# TODO: vamos alterar essas configurações quando fizermos o deploy do nosso app
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }