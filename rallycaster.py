from flask import render_template
from rallycaster import app
from rallycaster.config import config


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    config.set_configuration()
    app.run()
