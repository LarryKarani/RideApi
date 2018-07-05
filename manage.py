import os
from FlaskApp.api.app import create_app

environment = os.environ.get('config')
app = create_app(environment)

if __name__ == '__main__':
    app.run()
    