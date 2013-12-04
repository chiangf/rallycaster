from flask import render_template, g
from rallycaster import app
from rallycaster.interfaces.authentication import auth_required


@app.route('/')
@auth_required()
def index():
    return render_template('index.html', user=g.user)


if __name__ == '__main__':
    if app.debug:
        app.run(use_debugger=True, use_reloader=False)
    else:
        app.run(debug=True)
