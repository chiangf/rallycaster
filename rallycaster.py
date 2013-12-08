from rallycaster import app


if __name__ == '__main__':
    if app.debug:
        app.run(use_debugger=True, use_reloader=False)
    else:
        app.run(debug=True)
