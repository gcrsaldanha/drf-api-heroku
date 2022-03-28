import os
from tamarcado.settings.base import *

# When DEBUG is True and ALLOWED_HOSTS is empty, the host is validated against ['.localhost', '127.0.0.1', '[::1]'].
ALLOWED_HOSTS = []
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '0.0.0.0'
EMAIL_PORT = 1025