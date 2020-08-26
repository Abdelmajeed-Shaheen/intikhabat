import dj_database_url
import dotenv
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)