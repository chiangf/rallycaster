(function() {
    var App = window.App = {
        routers: {},
        models: {},
        collections: {},
        views: {},
        controllers: {},
        events: {}
    };

    App.router = {};

    // Stores authenticated user object, set in begin.html
    App.user = null;
})();
