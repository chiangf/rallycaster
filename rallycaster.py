from flask import render_template
from rallycaster import app
from rallycaster.config import config


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    config.set_configuration()

    if app.debug:
        app.run(use_debugger=True, use_reloader=False)
    else:
        app.run(debug=True)
