from rallycaster import create_app


if __name__ == '__main__':
    app = create_app()

    if app.debug:
        app.run(use_debugger=True, use_reloader=False)
    else:
        app.run(debug=True)
