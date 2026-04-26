import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'cmsblobstorageacc'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'rHl65DWAse8YuNxvq8wYb+GYDoBxMLjIdrJWpmBx7/uxiH6TfnZeSUhaSQpXq49en1HzP76QX4fv+ASt0DnSgw=='
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'images'

    SQL_SERVER = os.environ.get('SQL_SERVER') or 'cms-database-server.database.windows.net'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'free-sql-db-6493018'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'cms-admin'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'Raj1234$'
    # Below URI may need some adjustments for driver version, based on your OS, if running locally
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://cms-admin:Raj1234$@cms-database-server.database.windows.net:1433/free-sql-db-6493018?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&LoginTimeout=30'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### Info for MS Authentication ###
    ### As adapted from: https://github.com/Azure-Samples/ms-identity-python-webapp ###
    CLIENT_SECRET = "~NS8Q~J5BtKpfKhaDYlH99OJBg-65b1SJZpwPayc"
    # In your production app, Microsoft recommends you to use other ways to store your secret,
    # such as KeyVault, or environment variable as described in Flask's documentation here:
    # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    # if not CLIENT_SECRET:
    #     raise ValueError("Need to define CLIENT_SECRET environment variable")

    # AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app, else put tenant name
    AUTHORITY = "https://login.microsoftonline.com/f958e84a-92b8-439f-a62d-4f45996b6d07"

    CLIENT_ID = "46c293e5-9a83-4781-a6bf-fd9260577303"

    REDIRECT_PATH = "/getAToken"  # Used to form an absolute URL; must match to app's redirect_uri set in AAD

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.Read"]  # Only need to read user profile for this app

    SESSION_TYPE = "filesystem"  # Token cache will be stored in server-side session
