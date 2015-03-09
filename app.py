from sample_api import app
from sample_api import create_app

if __name__ == '__main__':
    create_app()
    app.run(debug=True)